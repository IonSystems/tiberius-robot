import subprocess

sqlc = subprocess.call("sqlc -r data_service=8001 db", shell = True)
iterator =  iter(sqlc.stdout.readline, b"")

for line in iterator:
    print line

sqlc2 = subprocess.Popen("CREATE TABLE test_table4 (id int primary key, column varchar(20))")


iterator =  iter(sqlc2.stdout.readline, b"")

for line in iterator:
    print line

