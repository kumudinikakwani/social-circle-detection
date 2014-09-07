try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Detecting social cirles in ego networks',
    'author': 'Kumudini',
    'url': 'https://github.com/kumudinikakwani/social-circle-detection',
    'author_email': 'kumudinikakwani13@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['SocialCirclesDetection'],
    'scripts': [],
    'name': 'SocialCirclesDetection'
}

setup(**config)
