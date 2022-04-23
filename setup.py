"""
Inside setup.py we specify the code which will make our project installable! This means that we can 
build a distribution file and isntall that in another environment, just like with 'pip'. THis makes
deploying our project exactly the same as installing any other library, so we will utilaze all the 
standard Pythong tools to manage everything
"""

from setuptools import find_packages, setup

setup(
    name='app',
    version='1.0.0',
    packages=find_packages(),  # packages tells Python what package directories (and the Pyhton files they contain) to include
    include_package_data=True, # includes OTHER files such as static and templates directories
    zip_safe=False,
    install_requires=[
        'flask',
        'Flask-SQLAlchemy',
    ],
)

