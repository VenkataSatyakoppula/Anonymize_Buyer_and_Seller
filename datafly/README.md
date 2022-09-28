# Python Datafly

Datafly is a greedy heuristic algorithm which is used to anonymize a table in order to satisfy k-anonymity.

Currently supports the CSV format.

Python implementation of the Datafly algorithm. Finds a k-anonymous representation of a table.


#### Domain Generalization Hierarchy file format

For each Quasi Identifier attribute, a corresponding Domain Generalization Hierarchy must be specified, which is used to generalize the attribute values.

#### command to execute
```
$ python datafly.py -pt "example/Buyer_data_for_data_fly.csv" -qi "Age" "Zip Code" -dgh "conf/age_hierarchy.csv" "conf/zip_hierarchy.csv" -k 3 -o "example/Buyer_data_after_datafly.csv"
```


### 2,3
### 4-12
### 16