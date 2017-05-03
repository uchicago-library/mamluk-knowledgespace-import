# mamluk-knowledgespace-import
This is source code for transforming PDFs from the Mamluk journal project to Simple Archive Format import objects for knowledgespace.uchicago.edu

Step 1
======

The first step in this project was to extract the useful metadata from the PDFs retrieved from the primary stakeholder. After extraction occured, the data needed to be entered into a report for all stakeholders to review.

How I solved the first requirement:

I used the third-party python library PyPDF2 after a quick google search resulted in several StackOverflow discussions pointint to that library. After checking the [project github][https://github.com/mstamy2/PyPDF2], I am comfortable in stating that this project is still active and so still safe to use for this task.

- https://www.blog.pythonlibrary.org/2012/07/11/pypdf2-the-new-fork-of-pypdf/
- https://pythonhosted.org/PyPDF2/
- http://stackoverflow.com/questions/32667398/best-tool-for-text-extraction-from-pdf-in-python-3-4

How I solved the second requirement:

I used the python library csv to write a dict to a CSV file

The output is available at 

https://docs.google.com/spreadsheets/d/1SMuorHqBHLjXySrj4kJqf-Tzo8b-K-W4cEwWFkdvuaQ/edit#gid=1327477525
