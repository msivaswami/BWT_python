# bwt_package/setup.py

from setuptools import setup, find_packages

setup(
    name='bwt_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'bwt_script = bwt_package.bwt_script:main',
        ],
    },
)
