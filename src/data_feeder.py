import sys

if len(sys.argv) != 8:
    print("Incorrect parameters, received:", sys.argv[1:])
    print("Expected parameters: dry_run, host, port, username, password,"
          "dbname, data_folder")
    exit(0)

_, dry_run, host, port, username, password, dbname, data_folder = sys.argv
if username == "unset" or password == "unset":
    username = None
    password = None

print(dry_run, host, port, username, password, dbname, data_folder)

