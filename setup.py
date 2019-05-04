from setuptools import setup, find_packages

from data_census.util.env import PROJECT_NAME


def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setup(
    name=PROJECT_NAME,
    version='0.0.1',
    description='Easy access to multisatpm data.',
    url=f'http://github.com/dmsul/{PROJECT_NAME}',
    author='Daniel M. Sullivan',
    author_email='sullydm@gmail.com',
    tests_require=[
        'pytest',
    ],
    packages=find_packages(),
    package_data={PROJECT_NAME.replace('-', '_'): ["py.typed"]},
    # include_package_data=True,        # To copy stuff in `MANIFEST.in`
    # install_requires=dependencies,
    zip_safe=False,
)
