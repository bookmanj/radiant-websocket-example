import os

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

this = os.path.dirname(os.path.realpath(__file__))

def read(name):
    with open(os.path.join(this, name)) as f:
        return f.read()


setup(
    name='radiant-websocket-example',
    version='0.0.1',
    description='description',
    long_description=readme,
    author='Jay Perusse',
    author_email='bookman.jay@gmail.com',
    packages=['app_source'],
    install_requires=read('requirements.txt'),
    include_package_data=True,
    zip_safe=True,
    licence='MIT',
    keywords='example app snap linux ubuntu',
    test_suite='tests',
    scripts=['bin/radiant-websocket-example']
)
