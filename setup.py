from setuptools import setup, find_packages

setup(
    name='doctoruke',
    author='The Most Significant Bit',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'doctoruke=doctoruke:main',
        ],
    },
    install_requires=[
        'docopt',
        'bs4',
        'httpx',
        'eyeD3',

    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
