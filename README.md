## How to install MongoDB on ubuntu WSL
---

> **_Update Ubuntu Packages_**

```bash
sudo apt update
```

> **_Install MongoDB on the command line_**

https://dev.to/seanwelshbrown/installing-mongodb-on-windows-subsystem-for-linux-wsl-2-19m9

```bash
sudo apt-get install mongodb
# confirm with:
Y
```

* `mongod` - starts your local database server and runs it on the default port (27017)
* `mongo` runs the MongoDB shell-- allowing you to connect with the database and interact with it manually.


> **_Create some folders and persmissions_**

```bash
# go to your root directory
cd /

# the -p creates the parent folder(s) as well, if they don't exist already
sudo mkdir -p data/db 

# recursively give the proper permissions to the folders
sudo chown -R `id -un` data/db
```


> **_Setup alias for some commands_**

```bash
alias check_mongodb='sudo service mongodb status'
alias start_mongodb='sudo service mongodb start'
alias stop_mongodb='sudo service mongodb stop'
```

> **_Check the connection status_**
```bash
mongo --eval 'db.runCommand({connectionStatus: 1})'
```


> **_Other useful shell commands_**

```bash
# check if mongod is running by checking the Process
ps -e | grep 'mongod'


# check if mongod is running with netstat
netstat -an | grep 27017
```


## Basic MongoDB Queries
---


> **_Check out the databases and collections_**

```bash
# start up a new database by switching to it (creates it if it does not exist).
# The db does not exist until you create a collection
> use travel_db
> db
# show all current databases
> show dbs
# list all collections within the current database
> show collections
```

> **_Create a collection_**

```bash
> db.createCollection("destinations")
```


> **_Insert Data_**
```bash
# input data into a document (row):
> db.colelctionName.insert({key:value})

# Example:
> db.destinations.insert({"continent": "Europe", "country": "Italy", 
   "major_cities": ["Milan", "Rome", "Florence", "Turin", "Rome"]})
```

> **_Find Data_**
```bash
# return values within specific collection in a pretty way
> db.destinations.find().pretty()
# find specific document within a collections
> db.destinations.find({"key":value})
```

> **_Update Data_**

* The `update()` method takes two objects as its parameters, and it will only update the first entry that matches:
    - first Object: what document(s) to search from
    - second Object: what values to change

    - ```bash
      > db.collectionName.update()
      # Example:
      > db.destinations.update({"countr": "USA"}, {$set: {"continent": "Antarctica"}})
      ```

* The `updateMany()` method can be used to update multiple documents instead. 
This method will update all of the records that meet this given criteria.

    - ```bash
      > db.destinations.updateMany({"continent": "Europe"}, {$set: {"continent": "Antarctica"}})
      ```

* If the document being searched within a collection does not exists, the parameter `{upsert:true}` must be passed in order to create the nonexisting document.

    - ```bash
       > db.destinations.update({"country": "Brazil"}, {$set: {"capital": "Brasilia"}}, {upsert: true})
        ```

> **_Push Data to an Array_**

* The `$push` added command will add a value into an array. That will substitute the `$set` command

```bash
> db.destinations.update({"country": "Italy"}, {$push: {"major_cities": "Siena"}})
```

> **_Remove Data_**

* In order to delete the documents from a Mongo collection simply pass an empty object into the `remove()` method. Note that this command is extremely risky as **ALL DOCUMENTS** from the collection will drop and **ALL DATA** will be lost.

    - ```bash
      > db.destinations.remove({})
      ```

* Passing an object into the `remove()` method will stipulate what `{key:value}` pairing to search for. Adding the `justOne` parameter will remove only a single document. Without passing the `justOne` parameter, all documents matching the `{key:value}` pairing will be dropped from the collection.

    - ```bash
      > db.destinations.remove({"country": "USA"}, {justOne: true}) 
      ```

* The `drop()` method will delete the collection named from the database

    - ```
      > db.collectionName.drop()
      ```

* The `dropDatabase()` method will delete the whole database:

    - ```bash
      > db.dropDatabase()
      ```



## Miscellaneous
---

> **_Save an iPython sesion_**

```python
In [1] : import numpy as np
....
In [135]: counter=collections.Counter(mapusercluster[3])
In [136]: counter
Out[136]: Counter({2: 700, 0: 351, 1: 233})

# You want to save lines from 1 till 135 then on the same ipython session use this command

In [137]: %save test.py 1-135


# Or Append with -a 
In [137]: %save -a test.py 1-135

```

> **_Convert from `.py` to `.ipynb`_**

```bash
# you can simply rename it:
mv <file>.py <file>.ipynb

# or
# install p2j if you don't have it yet
p2j myscript.py
```

