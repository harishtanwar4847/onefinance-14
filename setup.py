from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in onefinance/__init__.py
from onefinance import __version__ as version

setup(
	name="onefinance",
	version=version,
	description="this is onefinance app",
	author="harish.tanwar@atriina.com",
	author_email="harish.tanwar@atriina.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
