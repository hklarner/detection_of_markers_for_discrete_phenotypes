

from biomarkers.factorization.integer_sets import IntegerSets


def test_is_factor():
    sets1 = IntegerSets(sets_of_integers=[[1], [2]])
    sets2 = IntegerSets(sets_of_integers=[[1, 3], [2, 3]])
    sets3 = IntegerSets(sets_of_integers=[[0, 3], [2, 3]])

    assert sets1.is_a_factor_of(sets2)
    assert not sets2.is_a_factor_of(sets1)
    assert not sets1.is_a_factor_of(sets3)


def test_equality():
    sets1 = IntegerSets(sets_of_integers=[[1], [2]])
    sets2 = IntegerSets(sets_of_integers=[[3], [4]])
    sets3 = IntegerSets(sets_of_integers=[[4], [3]])
    sets4 = IntegerSets(sets_of_integers=[[4], [3], [5]])

    assert sets1 != sets2
    assert sets1 != sets4
    assert sets2 == sets3

    sets5 = IntegerSets(sets_of_integers=[[1, 2], [4, 3]])
    sets6 = IntegerSets(sets_of_integers=[[3, 4], [2, 1]])

    assert sets5 == sets6


def test_multiplication():
    sets1 = IntegerSets(sets_of_integers=[[1], [2]])
    sets2 = IntegerSets(sets_of_integers=[[3], [4]])

    assert sets1 * sets2 == IntegerSets(sets_of_integers=[[1, 3], [1, 4], [2, 3], [2, 4]])
    assert len(sets1 * sets2 * sets1) == 6


def test_is_a_factor_of():
    sets1 = IntegerSets(sets_of_integers=[[1], [2]])
    sets2 = IntegerSets(sets_of_integers=[[1, 3], [2, 3]])
    sets3 = IntegerSets(sets_of_integers=[[1, 2], [2, 3]])

    assert sets1.is_a_factor_of(sets2)
    assert not sets1.is_a_factor_of(sets3)
