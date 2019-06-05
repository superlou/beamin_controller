#!/usr/bin/env python3
from distutils.core import setup

setup(name='beamin_controller',
      version='0.1.0',
      description='Beamin info-beamer controller',
      author='Louis Simons',
      author_email='lousimons@gmail.com',
      packages=['beamin_controller'],
      entry_points = {
        'console_scripts': ['beamin=beamin_controller.beamin:main',
                            'beamin_status=beamin_controller.status:main']
      },
      install_requires = [
        'asciimatics',
	'requests'
      ])
