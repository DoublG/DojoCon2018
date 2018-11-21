from setuptools import setup, find_packages

setup(
    version='0.20',
    author='Erik Woidt',
    author_email='erik@woidt.be',
    packages=find_packages(exclude='test'),
    name='Webhook',
    install_requires=['Flask', 'Flask-Login', 'pika', 'requests', 'jsonschema'],
    tests_require=['blinker'],
    include_package_data=True,
    url=''
)