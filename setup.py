from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "churn_pred",
    version = "0.1",
    author = "Bargav Jagatha",
    author_email = "jbargav025@gmail.com",
    description = "A package to predict churn",
    packages = find_packages(),
    install_requires = requirements
)