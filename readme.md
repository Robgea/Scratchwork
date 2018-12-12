# CIK scanning project

Quovo Project Readme:


Inside this folder are the Readme, the script itself, and some example outputs.


Workflow of the Program:


- First it prompts the user to enter a list of CIKs to put through the system. It does a basic error check to make sure the CIKs are valid inputs but little else.

- Then it passes each one off in turn to a program that uses the Requests Module to access a search of every 13F report associated with that CIK. If the program cannot find a 13F report it prints that back to the user. 

- It then uses Beautiful Soup to find the link on the page to the most recent filing, and passes that to another program which then finds the full text report associated with the 13F filing.

- Then Beautiful Soup parses the XML and generates a TSV with the organizations's name, the date of the filing, and the complete holdings of the organization categorized by type of stock. Occasionally this will flag an error because a company will have a name that cannot be written to a TSV file. I have written an error catcher to resolve that. If I were to spend more time on this program I would  create a regex script to scan for invalid characters and remove them. 

- It does this for every CIK given until done.


How to add dates:

- I thought about adding a date search, and have a rough method of doing so written, but didn't add it in the core program because I barely tested it. The workflow for that would be:

- Instead of creating a string when asking the user for CIKs to lookup I would create Tuples. The first part of the tuple would be the CIK, the second part would be a date. The user could choose to enter a date or leave the date field blank (which would default to either 0 or today's date, depending on how complicated I wanted to make the program.)  When this tuple was passed to the function that would parse the list of 13F reports instead of taking the first item in the list it would scan through the links for the first item before the date inputted via the date information attached to the entry.