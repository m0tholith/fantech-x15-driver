from setuptools import find_packages, setup

setup(
    name="fantech-x15-driver",
    version="1.0",
    # Modules to import from other scripts:
    packages=find_packages(),
    # Executables
    scripts=["fantech-x15-driver"],
)
