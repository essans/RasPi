### Things to remember when using clustercmd.py


Chaining commands:

```
./clustercmd -c 'cd code/python && sudo cp /etc/hosts test_hosts'

```

```
./clustercmd -c 'cd code && sudo mkdir python'

./clustercmd -c 'sudo chmod -R 0777 code'   #full permissions


```

Resources:
https://docs.fabfile.org/en/2.6/api/connection.html
