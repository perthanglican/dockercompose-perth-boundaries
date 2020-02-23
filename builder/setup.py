from setuptools import setup, find_packages

setup(
    author="Grahame Bowland",
    author_email="grahame@oreamnos.com.au",
    description="Anglican Diocese of Perth - Parish boundary generator",
    license="GPL3",
    url="https://github.com/grahame/sedge",
    name="labyrinth",
    version="1.0.0",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    entry_points={
        'console_scripts': [
            'labyrinth = labyrinth.cli:main',
        ],
    },
)
