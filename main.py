from antlr4 import *

import os

from Code.Database import export_db
from Code.EstListener import EstListener
from Gen20.Java20Lexer import Java20Lexer
from Gen20.Java20Parser import Java20Parser

print('Extended Symbol Table Builder v1\n')
input_folder = input('Enter project relative path (e.g. Projects/SampleTest): ')
print(f'Scanning {input_folder} directory and its subdirectories for java source code files...')

# Create an empty list to store the relative paths of .java files
java_files = []

# Loop through the files and subdirectories in the input directory
for root, dirs, files in os.walk(input_folder):
    # Loop through the files
    for file in files:
        # Check if the file has a .java extension
        if file.endswith(".java"):
            # Join the root and file name to get the relative path
            path = os.path.join(root, file)
            # Append the path to the list
            java_files.append((path, file))

project_est = []
for f in java_files:
    print(f'\nGenerating EST for {f[1]}...')

    # Reading the Java source code
    input_stream = FileStream(f[0])

    # Creating a lexer object
    lexer = Java20Lexer(input_stream)

    # Creating a token stream
    stream = CommonTokenStream(lexer)

    # Creating a parser object
    parser = Java20Parser(stream)

    # Creating a parse tree
    tree = parser.compilationUnit()

    # Creating a listener object
    listener = EstListener(f[1])

    # Walking the parse tree
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    # Printing the symbol table
    listener.print_entities()

    # Finalize database (Convert scope name to scope id)
    # If you want to scope names instead of scope id, comment this line
    listener.finalize_est()

    # Add current file est to project est
    project_est.extend(listener.est)

# Export EST database
print(f'\nTotal {len(project_est)} Entities extracted from project')
print('Exporting EST to database, Please wait...')
export_db(project_est, f'{input_folder.split("/")[-1]}.db')
