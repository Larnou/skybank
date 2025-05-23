from invoke import task

@task
def flake8(ctx):
    # запуск: inv flake8
    ctx.run("poetry run flake8 src/")

@task
def black(ctx):
    # запуск: inv black
    ctx.run("poetry run black src/")

@task
def mypy(ctx):
    # запуск: inv mypy
    ctx.run("poetry run mypy src/")

@task
def isort(ctx):
    # запуск: inv isort
    ctx.run("poetry run isort src/")

# @task
# def test(ctx):
#     ctx.run("pytest tests/")