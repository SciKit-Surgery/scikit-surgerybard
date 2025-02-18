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
    description='scikit-surgerybard is a Basic Augmented Reality Demo (BARD)'
                'based on scikit-surgery (SNAPPY)',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/SciKit-Surgery/scikit-surgerybard',
    # Authors: Miguel Xochicale, Thomas Dowrick, Stephen Thompson, Matt Clarkson
    author='Stephen Thompson',
    author_email='s.thompson@ucl.ac.uk',
    license='BSD-3 license',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',


        'License :: OSI Approved :: BSD License',


        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],

    keywords='medical imaging',

    packages=find_packages(
        exclude=[
            'doc',
            'tests',
            'data',
        ]
    ),

    install_requires=[
        'numpy',
        'glob2',
        'pyside6>=6.5.1.1',
        'opencv-contrib-python-headless>=4.2.0.32',
        'scikit-surgerycore>=0.6.10',
        'scikit-surgerycalibration>=0.2.5',
        'scikit-surgeryutils>=2.0.1',
        'scikit-surgeryvtk>=2.2.1',
        'scikit-surgeryarucotracker>=1.0.3',
    ],

    entry_points={
        'console_scripts': [
            'bardVideoCalibration=sksurgeryutils.ui.sksurgeryvideocalibration_command_line:main',
            'bardVideoCalibrationChecker=sksurgeryutils.ui.sksurgeryvideocalibrationchecker_command_line:main',
            'bardPivotCalibration=sksurgerycalibration.ui.pivot_calibration_command_line:main',
            'bardProcrustes=sksurgerybard.ui.bard_procrustes_command_line:main',
            'sksurgerybard=sksurgerybard.ui.sksurgerybard_command_line:main',
        ],
    },
)
