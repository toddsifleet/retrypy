from distutils.core import setup

import retrypy

with open('README.rst') as f:
    long_description = f.read()

setup(
    description='Python retry utility',
    long_description=long_description,
    name='retrypy',
    version=retrypy.__version__,
    author='Todd Siflet',
    author_email='todd.siflet@gmail.com',
    py_modules=['retrypy.retry'],
)
