from setuptools import setup

version = '0.1.0dev2'

with open('README.md', 'r') as f:
    long_description = f.read()

DEPENDENCIES = [
    'pyyaml',
    'python-consul'
]

setup(
    name='py-viper',
    version=version,
    description='Python viper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['viper'],
    author='shaneing',
    author_email='z.shane.ing@gamil.com',
    url='https://github.com/shaneing/python-viper',
    install_requires=[DEPENDENCIES],
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
