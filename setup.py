from setuptools import setup
setup(
    name = 'downloadmp3',
    version = '0.0.1',
    packages = ['downloadmp3'],
    entry_points = {
        'console_scripts': [
            'downloadmp3 = downloadmp3.__main__:main'
        ]
    })
