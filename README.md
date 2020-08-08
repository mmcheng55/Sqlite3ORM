**Sqlite3 ORM**<br>
It is a wrapper for SQLite3.
For Example:

Creating a table using Table object:
```python
from sqlite3_orm import *
from sqlite3_orm.Table import Table

database = Database(":memory:")
Record = Table(database, "Records", record_1="TEXT", id="INTEGER")
```

Create a record:
```python
    Record.add(record_1="Record 1", id=1)
```

Get / Fetch a data:
```python
    Record.fetch(record_1="Record 1")
```

Delete a record:
```python
    Record.delete(record_1="Record 1")
```

Update:
```python
    Record.update("record_1", "Record 2", id=2)
```

Add Multiple Row:
```python
    Record.add_multiple([["Record 2", 2], ["Record 3", 3]])
```