from setuptools import setup, find_packages
import os
import pypandoc

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def brag_dir():
    return os.environ.get('BRAG_DIR', os.path.expanduser('~/.brag'))

with open('README.rst', 'r') as f:
    readme = f.read()
    import pypandoc

= pypandoc.convert('somefile.md', 'rst')

setup(
    name='bragly',
    version='0.1.0',
    description='A small tool to remind yourself of your day-to-day accomplishments',
    long_description = readme,
    url='http://github.com/huntcsg/bragly',
    author='Hunter Senft-Grupp',
    author_email='huntcgs@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
       'console_scripts': [
            'brag = bragly.__main__:main',
            'brag-util = bragly.__main__:util'
        ], 
    },
    install_requires=[
      'arrow',
      'six',
    ],
    package_data={'bragly': ['config_example/*.ini']},
    include_package_data=True,
    tests_require=[
        'nose',
        'coverage',
    ],
    test_suite='nose.collector',
)
