import glob
from distutils.core import setup

the_scripts = glob.glob('scripts/*')

setup(
	name = 'mython',
	version = '0.0.1',
	author = 'Mark Carter',
	scripts = the_scripts,
	packages = ['mython'],
)
