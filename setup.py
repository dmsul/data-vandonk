from setuptools import setup, find_packages

from data_vandonk.util.env import PROJECT_NAME


def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


description = 'Access to van Donkelaar et al. data.'

dependencies = [
    'econtools',
    'xarray',
    'pandas',
]

setup(
    name=PROJECT_NAME,
    version='0.0.1',
    description=description,
    long_description=readme(),
    url=f'http://github.com/dmsul/{PROJECT_NAME}',
    author='Daniel M. Sullivan',
    author_email='sullydm@gmail.com',
    packages=find_packages(),
    tests_require=[
        'pytest',
    ],
    # include_package_data=True,        # To copy stuff in `MANIFEST.in`
    # install_requires=dependencies,
    package_data={PROJECT_NAME.replace('-', '_'): ["py.typed"]},
    zip_safe=False,
)
