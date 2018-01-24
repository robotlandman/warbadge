from setuptools import setup
from pip.req import parse_requirements

install_requires = ''
with open('requirements.txt') as fp:
        install_requires = fp.read()
setup(
    name='warbdage_app',
    version='1.0',
    long_description=__doc__,
    packages=['warbadge_app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires
)
