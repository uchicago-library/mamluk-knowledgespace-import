
from setuptools import setup

setup(name='mamlukimport',
      version='0.1',
      description='A tool to parse the PDFs from the Mamluk Studies Journal for metadata and generate SAF imports for knowledgespace',
      author='Tyler Danstrom',
      author_email='tdanstrom@uchicago.edu',
      url='https://github.com/uchicago-library/mamluk-knowledgespace-import/',
      packages=['mamlukimport'],
      scripts=['bin/build_safs.py', 'bin/extractor.py'],
      install_requires=['python-magic', 'PyPDF2', 'pylint']
     )
