Simple folder synchronization program.

-It handles subdirectories by using os.walk() to traverse the entire directory of the source folder, allowing for nested directory synchronization;
-Before copying files, it checks if the files in the replica folder exists and compares their MD5 hashes to determine if they need to be updated.

Running the script from the command line:
Example: python folder_sync.py /path/to/source /path/to/replica 60 /path/to/logfile.log
