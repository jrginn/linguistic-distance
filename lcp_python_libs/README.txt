Last updated: 1/5/22
Last author of README.txt: Vivian D'Souza

On README:
Please when any major change to the package as a whole (ie: file naming convention, directory changes)
update the README accordingly. Update the "Last updated" to the date of the change of the README file,
and put your name on it so we can be able to know who to ask questions to.

On the contents of the package:

This package contains the code for the Linguistic Distance Project.
It is organized into classes, which one imports into a file such as a 
juypternotebook file or .py file.

To import, you must know where the folder is located. For instance, if your 
current working directory was "dir", and it contained:

"""
- file.py
- lcp_python_libs
- someotherfile.txt
"""

... and you wanted to import a class from lcp_python_libs into "file.py", you would
write (in file.py):

"""
# importing package from same directory
# # # # 

from lcp_python_libs.[FILE_NAME] import [CLASS]

"""

as an example:

"""
# importing package from same directory
# # # # 

from lcp_python_libs.Parser import Parser

"""

When the package folder is in a different directory, things
can get a bit tricky. One may want to use relative file
addressing. See: 
https://stackoverflow.com/questions/49100540/importing-a-class-in-another-folder

On updating the package:

For any major changes, please first create a branch in the Git repo and test the files you
change. Then, merge the branches. Please do not push onto main directly, as this may cause
issues.

Formatting of variable names:
- Name the variable as you wish, but prepend the data type with an underscore.
- For instance, instead of "count", you would write iCount"
- Look here: https://en.wikipedia.org/wiki/Hungarian_notation, specifically "Systems Hungarian Notation"

Changelog:

1/5/2022
Added functionality to process translations through dictionaries, in order to store translations for future reference.
See dictGetLangTransToEng and dfMakeAlignDfFromDict in SheetMaker.py
