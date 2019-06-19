from invoke import task
import os
import shutil
from letra import __version__

def black(c, check):
    cmd = f"black . --line-length=79 {'--check' if check is True else ''}"
    return c.run(cmd)


@task(aliases=["f"])
def format(c):
    return black(c, False)


@task(aliases=["cf", "fc"])
def check_format(c):
    return black(c, True)


@task(aliases=["t"])
def test(c):
    return c.run("pytest")


@task(aliases=["l", "lp"])
def lint(c):
    return c.run("pycodestyle .")


@task()
def clean_test_reports(c):
    shutil.rmtree(".test-reports/", ignore_errors=True)
    shutil.rmtree(".coverage/", ignore_errors=True)
    shutil.rmtree(".testresults/", ignore_errors=True)
    shutil.rmtree(".coverageresults/", ignore_errors=True)
    os.remove(".coverage")


@task(aliases=["c"], pre=[clean_test_reports])
def clean(c):
    pass

@task(aliases=["pv", "sv"])
def print_version(c):
    return print(__version__)
