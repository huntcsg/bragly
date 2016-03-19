from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='bragly',
    version='0.1.0',
    description='A small tool to remind yourself of your day-to-day accomplishments',
    long_description = read('README.md'),
    url='http://github.com/huntcsg/bragly',
    author='Hunter Senft-Grupp',
    author_email='huntcgs@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
       'console_scripts': [
            'brag = bragly.__main__:main',
        ], 
    },
    install_requires=[
      'arrow',
      'six',
    ], 
    tests_require=[
        'nose',
        'coverage',
    ],
    test_suite='nose.collector'
        
)
