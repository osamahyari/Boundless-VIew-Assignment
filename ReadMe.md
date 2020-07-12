
The _IDs of the annotations being inserted to the database are their respective IDs in the given file plus the file prefix, so that different annotations from different files, but have the same ID can have different _IDs.

Duplicates found are being removed.

Annotation duplicates are determined with their image_id and field_id as agreed.

Image duplicates are determined by their file name.

The Annotation's images and fields are being referenced.

To run the script use the following command 
```
python3 src/main.py '0' 'localhost' '27017' 'unset' 'unset' 'cheques' '1' 'json_files'
```
where the parameters are as follows:
`dry_run, host, port, username, password, dbname, cleandb, data_folder`
Dry run was to print the records being sent to the database instead of implementing any changes to the database, it haven't been implemented due to shortage of time.

Username and password are default parameters are unset so it would take their default value which is 0.

The docker part haven't been tested yet due to virtualization not being available on my windows machine, but here are the commands to run it.
```
cd <Boundless-View-Assignment dir>
docker build -t feeder . 
docker run -p 8888:8888 feeder
```

where <Boundless-View-Assignment dir> is the location where you clone the repository. 
