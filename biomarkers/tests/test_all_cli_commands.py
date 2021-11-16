import pytest

from click.testing import CliRunner

from biomarkers.cli.main import main


@pytest.mark.parametrize("args", [
    "problem-create --bnet n7s3 --exact --phenotype v1",
    "problem-create --bnet n7s3 --phenotype v1 --forbidden v2,v3 --problem n7s3_problem.json",
    "problem-create --bnet n7s3 --phenotype v1=1,v2=1 --forbidden v2,v3 --problem n7s3_problem.json",
    "problem-create --bnet n7s3 --phenotype v1=1,v2=1 --max-markers 1 --problem n7s3_problem.json",
    "problem-create --bnet n7s3 --phenotype v1=1,v2=1 --max-steady-states 2 --problem n7s3_problem.json",
])
def test_problem_create(args):
    runner = CliRunner()
    result = runner.invoke(main, args)
    assert result.exit_code == 0
