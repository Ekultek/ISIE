from setuptools import find_packages, setup

from lib.settings import VERSION


setup(
    name="isie",
    version=VERSION,
    packages=find_packages(),
    url="https://badassarmy.org",
    author="Ekultek",
    author_email="god_lok1@protonmail.com",
    description="Hoe swag (InfoSlut Image Editor)",
    license="GPLv3",
    scripts=["isie"],
    install_requires=open("requirements.txt").read().split("\n")
)