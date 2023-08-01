from setuptools import setup, find_packages

setup(
    name="dovali",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "pytest",
        "pygithub"
    ],
    entry_points='''
        [console_scripts]
        dovali=cli.main:cli
    '''
)
