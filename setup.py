from setuptools import setup, find_packages


setup(
    name='password-sprayer',
    version='0.0.1',
    description='Simple password sprayer written in Python',
    maintainer='@patamechanix',
    license='MIT',
    url='https://github.com/patamechanix/python-password-sprayer',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=find_packages('src'),
    entry_points={
        'console_script': [
            'password-sprayer = password_sprayer.__main__:main'
        ]
    }
)
