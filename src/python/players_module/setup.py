#!/usr/bin/env python
from setuptools import setup, find_packages


def get_dependencies(requirements_file='requirements.txt'):
    with open(requirements_file, 'r') as f:
        dependencies = [dep for dep in f.read().splitlines() if dep]
    return dependencies


setup(
    name='players',
    version='0.1.0',
    python_requires='>=3.9.11',
    packages=find_packages(),
    package_dir={
        'walterplayers': './walterplayers',
    },
    install_requires=get_dependencies(),
    extras_require={'dev': [get_dependencies('dev-requirements.txt')]},
)
