# Introduction

This is a tool that takes PDF files, allows the user to extract metadata form those pdfs into a CSV so taht stakeholder can edit the metadata in a single place, then from that CSV file and a location of the pdf files create a series of SAFS

## Quickstart

1. create a virtualenv
1. git clone this repo
1. cd into the repo directory
1. activate the virtualenv
1. run ```python setup.py install```
1. call either extractor.py on the pdf directory to extract the metadata or build_safs.py on the csv metadata file and the pdfs directory to generate SAFs


