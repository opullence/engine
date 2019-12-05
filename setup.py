from setuptools import find_namespace_packages, setup

with open("README.md") as f:
    readme = f.read()

with open("requirements/production.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="opulence.engine",
    version="0.0.3",
    description="Core engine for opulence",
    long_description=readme,
    author="Opulence",
    author_email="contact@opulence.fr",
    url="https://github.com/opullence/engine",
    license=license,
    packages=find_namespace_packages(include=["opulence.*"]),
    entry_points={"console_scripts": ["opulence-engine=opulence.engine.__main__:main"]},
    install_requires=requirements,
    python_requires=">=3.6.*, <4",
)
