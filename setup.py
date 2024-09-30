from setuptools import setup
from setuptools import find_packages

long_description= """
# jlu
A collection of functions to make JupyterLab notebooks cleaner
"""

required = [
    "requests", 
    "numpy",
    "Pillow",
    "pydub",
    "moviepy"
]

setup(
    name="jlu",
    version="0.0.1",
    description="A collection of functions to make JupyterLab notebooks cleaner",
    long_description=long_description,
    author="Jacob Hart",
    author_email="jacob.dchart@gmail.com",
    url="https://github.com/arvest-data-in-context/jlu",
    install_requires=required,
    packages=find_packages()
)