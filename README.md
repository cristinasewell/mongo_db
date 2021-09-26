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
# show all current databases
> show dbs
# list all collections withing the current database
> show collections
```

> **_Insert Data_**
```bash
# input data into a document (row):
> db.colelctionName.insert({key:value})

# Example:
> db.destination.insert({"continent": "Europe", "country": "Italy", 
   "major_cities": ["Milan", "Rome", "Florence", "Turin", "Rome"]})
   WriteResult({ "nInserted" : 1 })
```

> **_Find Data_**
```bash
# return values within specific collection in a pretty way
> db.destinations.find().pretty()
# find specific dobument withing a collections
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

* The `updateMany()` method can be used to update multiple documents intead. 
This method will update all of the records that meet this given criteria.

    - ```bash
      > db.destinations.updateMany({"continent": "Europe"}, {$set: {"continent": "Antarctica"}})
      ```

* If the document being searched withing a collection does not exists, the parameter `{upsert:true}` must be passed in order to create the nonexisting document.

    - ```bash
       > db.destinations.update({"country": "Brazil"}, {$set: {"capital": "Brasilia"}}, {upsert: true})
        ```

> **_Push Data to an Array_**

* The `$push` added command will add a value into an array. That will substitute the `$set` command

```bash
> db.destinations.update({"country": "Italy"}, {$push: {"major_cities": "Siena"}})
```

> **_Remove Data_**

* In order to delte the documents from a Mongo collection simply pass an empty object into the `remove()` method. Note that this command is extremely riscky as **ALL DOCUMENTS** from the collection will drop and **ALL DATA** will be lost.

    - ```bash
      > db.destinations.remove({})
      ```

* Passing an object into `remove()` method will stipulate what `{key:value}` paring to search for. Adding the `justOne` parameter will remove only a single document. Without passing the `justOne` parameter, all documents mathching the `{key:value}` pairing will be dropped from the collection.

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