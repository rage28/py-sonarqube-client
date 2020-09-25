"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))


def get_long_description() -> str:
    """Get the module description

    Returns:
        Project description
    """
    with open(path.join(here, 'README.asciidoc'), encoding='utf-8') as readme_file:
        long_description = readme_file.read()
    return long_description


def get_version() -> str:
    """Get the module version

    Returns:
        Module version
    """
    with open(path.join(here, 'version.txt')) as version_file:
        version_str = version_file.readline().rstrip()
    return version_str


def get_install_requires():
    """Get required external dependencies

    Returns:
        List of required dependencies
    """
    with open(path.join(here, 'requirements.txt')) as requirements_file:
        reqs = [line.rstrip() for line in requirements_file.readlines()]
    return reqs


setup(
    name='sonarqube-client',

    # https://packaging.python.org/en/latest/single_source_version.html
    version=get_version(),

    description='SonarQube Client',
    long_description=get_long_description(),
    url='https://github.com/rage28/py-sonarqube-client',
    author='Raghavendra Bhuvan',
    author_email='rage28@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development'
    ],

    keywords='sonarqube sonar',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),

    # https://packaging.python.org/en/latest/requirements.html
    install_requires=get_install_requires(),
    extras_require={},
    package_data={},

    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    data_files=[],
)
