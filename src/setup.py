from setuptools import find_packages, setup

setup(
    name="Network-Analysis-Library",
    version="0.1",
    description="Library for NAL project",
    author="Group 8",
    packages=find_packages("nal"),
    include_package_data=True,
    install_requires=[
        "matplotlib",
        "networkx",
        "numpy",
        "pandas",
        "powerlaw",
        "scipy",
        "tabulate",
    ],
)
