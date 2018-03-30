#!/usr/bin/env python

from setuptools import setup, find_packages


with open('README.md') as readme_file:
    README = readme_file.read()


install_requires = [
    'chalice==1.1.1',
    'pyyaml',
    'marshmallow'
]

setup(
    name='wallice',
    version='0.1.2',
    description="Opinionated AWS Lambda web framework",
    long_description=README,
    author="Jan Aaron Angelo T. Lee",
    author_email='janaaronlee@gmail.com',
    url='https://github.com/janaaronlee/wallice',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    license="MIT License",
    package_data={'chalice': ['*.json']},
    include_package_data=True,
    zip_safe=False,
    keywords='chalice',
    entry_points={
        'console_scripts': [
            'wallice = wallice.cli:main',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
)
