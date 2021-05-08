from setuptools import setup

setup(
    name='gphoto-scrapper',
    version='0.1',
    packages=['gphoto_scrapper'],
    url='',
    license='GPL-v3',
    author='Daniel Vincze',
    author_email='vincze.daniel96@gmail.com',
    description='Download your photos and videos from Google Photos using the photoslibrary API',
    entry_points={
        'console_scripts': [
            'gphoto-scrapper = gphoto_scrapper.main:main'
        ]
    }
)
