from setuptools import setup

import retrypy

with open('README.rst') as f:
    long_description = f.read()

setup(
    description='Python retry utility',
    long_description=long_description,
    name='retrypy',
    version=retrypy.__version__,
    author='Todd Sifleet',
    author_email='todd.siflet@gmail.com',
    packages=['retrypy'],
    zip_safe=True,
    license='MIT',
    url='https://github.com/toddsifleet/retrypy',
)
