from setuptools import setup


setup(
    name='jsonlight',
    versioning='dev',
    setup_requires='setupmeta',
    extras_require=dict(
        test=['pytest', 'pytest-cov'],
    ),
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://yourlabs.io/oss/jsonlight',
    include_package_data=True,
    license='MIT',
    keywords='cli',
)
