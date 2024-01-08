import os

from Code.Database import export_db
from Code.EstListener import EstListener
from Code.RefListener import RefListener
from Code.FileScanner import scan_file

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
            # Append the path to the list
            java_files.append((path, file))

project_est = []

# First iteration: Scan all files for declarations
for f in java_files:
    print(f'Generating EST for {f[1]}...')

    # Creating a listener object
    entity_listener = EstListener(f[1], input_folder.split('\\')[0])

    # Add current file est to project est
    project_est.extend(scan_file(f, entity_listener))

# Second iteration: Scan all files and database for references
for f in java_files:
    print(f'Completing EST for {f[1]}...')

    # Walk tree for references
    reference_listener = RefListener(project_est)

    # Complete current file est
    project_est.extend(scan_file(f, reference_listener))


# Export EST database
print(f'\nTotal {len(project_est)} Entities extracted from project')
print('Exporting EST to database, Please wait...')
export_db(project_est, f'{input_folder.split("/")[-1]}.db')
