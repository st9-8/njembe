from njembe import VERSION
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as ld:
	long_description = ld.read()

EMAIL = 'stephanefedim@gmail.com'
DESCRIPTION = 'A simple tool to help us to document our strong command line processes'

setup(
	name='njembe',
	author='st9_8',
	version=VERSION,
	author_email=EMAIL,
	description=DESCRIPTION,
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/stephane98/njembe',
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
        "Operating System :: Unix OS",
        "Natural Language ::  English",
        "Natural Language :: French"
	],
	scripts=['./scripts/nj', './scripts/njembe'],
	packages=find_packages(),
	package_data={'njembe': ['config.ini', 'njembe.db']},
    install_requires=[
        'peewee',
        'configparser',
    ],
	python_requires='>3.6'
)