""" Setup
"""
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

exec(open('geffnet/version.py').read())
setup(
    name='geffnet',
    # version=__version__,
    description='(Generic) EfficientNets for PyTorch',
    url='https://github.com/rwightman/gen-efficientnet-pytorch',
    author='Ross Wightman',
    author_email='hello@rwightman.com',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Note that this is a string of words separated by whitespace, not a list.
    keywords='pytorch pretrained models efficientnet mixnet mobilenetv3 mnasnet',
    packages=find_packages(exclude=['data']),
    install_requires=['torch >= 1.4', 'torchvision'],
    python_requires='>=3.6',
)
