from distutils.core import setup, Extension

ext = Extension('_pyodb', ['pyodb.c'], 
	runtime_library_dirs=["/usr/local/lib"],
	library_dirs=["/usr/local/lib"],
	libraries=["odbc"])

setup(name='pyodb', 
	version='0.8', 
	author='Neil Moses',
	author_email='ndmoses@ntlworld.com',
	url='',
	py_modules=['pyodb'],
	ext_modules=[ext])
