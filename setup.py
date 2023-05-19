import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="mapperr",
    version="0.1.0",
    description="mapperr for mapping across dict and object, recursively",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mujdecisy/mapperr",
    keywords=["python", "mapper", "recursive mapping"],
    author="mujdecisy",
    author_email="mujdecisy@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["mapperr"],
    include_package_data=True,
    install_requires=[]
)