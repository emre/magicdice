from setuptools import setup, find_packages

setup(
    name='magicdice',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/emre/magicdice',
    license='MIT',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='A Python library to interact with the magic-dice game',
    install_requires=["steem", "requests"],
)