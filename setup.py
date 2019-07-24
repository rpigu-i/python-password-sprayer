from setuptools import setup, find_packages


setup(
    name='password-sprayer',
    version='3.0.0',
    description='Simple password sprayer written in Python',
    maintainer='https://github.com/rpigu-i',
    license='MIT',
    url='https://github.com/rpigu-i/python-password-sprayer',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=find_packages('src'),
    install_requires = [
        'requests>2.21.0',
        'pyyaml>5.0'
    ],
    entry_points={
        'console_script': [
            'password-sprayer = password_sprayer.__main__:main'
        ]
    }
)
