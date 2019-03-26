# coding=utf-8
"""
Setup for scikit-surgerybard
"""

from setuptools import setup, find_packages
import versioneer

# Get the long description
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='scikit-surgerybard',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='scikit-surgerybard is a Python package based on SNAPPY for Basic Augmented Reality Demo (BARD)',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/scikit-surgerybard',
    author='Mian Asbat Ahmad',
    author_email='rmapaah@ucl.ac.uk',
    license='BSD-3 license',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',


        'License :: OSI Approved :: BSD License',


        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],

    keywords='medical imaging',

    packages=find_packages(
        exclude=[
            'doc',
            'tests',
        ]
    ),

    install_requires=[
        'six>=1.10',
        'numpy>=1.11',
    ],

    entry_points={
        'console_scripts': [
            'sksurgerybard=sksurgerybard.__main__:main',
            'sksurgerybard-cl=sksurgerybard.ui.bard_camera_calibration_command_line:main',
            'sksurgerybard-app=sksurgerybard.ui.bard_camera_calibration_command_app:main',
        ],
    },
)