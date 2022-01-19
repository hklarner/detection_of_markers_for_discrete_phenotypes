import pytest
from click.testing import CliRunner

from biomarkers.cli.main import main


@pytest.mark.parametrize("args", [
    "problem-create --bnet n7s3 --phenotype v1=1,v2=1 --problem n7s3_problem.json",
    "problem-create --bnet n7s3 --phenotype v1,v2 --max-steady-states 2 --problem n7s3_problem.json",
])
def test_problem_create(args):
    runner = CliRunner()
    result = runner.invoke(main, args)
    assert result.exit_code == 0
