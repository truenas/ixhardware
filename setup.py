from distutils.core import setup
from setuptools import find_packages


setup(
    name="ixhardware",
    description="Detect iXsystems hardware",
    version="1.0",
    include_package_data=True,
    packages=find_packages(),
    license="GNU3",
    platforms="any",
)
