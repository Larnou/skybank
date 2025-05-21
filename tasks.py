from invoke import task

@task
def flake8(ctx):
    ctx.run("poetry run flake8 src/")

# @task
# def test(ctx):
#     ctx.run("pytest tests/")