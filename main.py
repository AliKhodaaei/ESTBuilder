import os

from Code.Database import export_db
from Code.EntListener import EntListener
from Code.RefListener import RefListener
from Code.FileScanner import scan_tree, build_tree

print('Extended Symbol Table Builder v1\n')
input_folder = input('Enter project relative path (e.g. Projects/SampleTest): ')

if not input_folder:
    input_folder = 'Projects/Hello'  # Start with a default folder

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
            # Append the (path, file) tuple to the list
            java_files.append((path, file))

# Create empty lists for project entities and references
project_est, project_entity_est, project_reference_est = [], [], []

# Create empty list for parse trees (we need to use them again)
trees = []

# First iteration: Scan all files for declarations
for (path, file) in java_files:
    print(f'Generating EST for {file}...')

    # Creating a listener object
    entity_listener = EntListener(filename=file, projectname=input_folder.split('\\')[0])

    # Build current file parse tree
    tree = build_tree(path)

    # Add current file parse tree to list of trees
    trees.append(tree)

    # Add current file est to project est
    project_entity_est.extend(scan_tree(tree, entity_listener))

# Second iteration: Scan all files and database for references
for (path, file) in java_files:
    print(f'Completing EST for {file}...')

    # Walk tree for references
    reference_listener = RefListener(project_entity_est)

    # Complete current file est
    project_reference_est.extend(scan_tree(trees.pop(0), reference_listener))

# Merge entities and references list
project_est.extend(project_entity_est)
project_est.extend(project_reference_est)

# Export EST database
print(f'\nTotal {len(project_est)} Entities extracted from project')
print('Exporting EST to database, Please wait...')
export_db(project_est, f'{input_folder.split("/")[-1]}.db')
