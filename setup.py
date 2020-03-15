from setuptools import setup
setup(
    name = 'downloadmp3',
    version = '0.0.4',
    packages = ['downloadmp3'],
    entry_points = {
        'console_scripts': [
            'dp3 = downloadmp3.__main__:main'
        ]
    })
