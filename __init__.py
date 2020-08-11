from . import errors, Table
import sqlite3


class Database:
    __slots__ = ["database", "c", "save", "strings", "ints", "real", "numeric"]

    def __init__(self, name: str):
        """
        Connect to a db
        :param name: Database root or filename.
        """
        self.database = sqlite3.connect(name, check_same_thread=False)
        self.c = self.database.cursor()
        self.save = self.database.commit
        self.strings = ["CHARACTER", "VARCHAR", "VARYING CHARACTER", "NCHAR", "NATIVE CHARACTER", "NVARCHAR", "TEXT", "CLOB"]
        self.ints = ["INT", "INTEGER", "TINYINT", "SMALLINT", "MEDIUMINT", "BIGINT", "UNSIGNED BIG INT", "INT2", "INT8"]
        self.real = ["REAL", "DOUBLE", "DOUBLE PRECISION", "FLOAT"]
        self.numeric = ["NUMERIC", "DECIMAL", "BOOLEAN", "DATE", "DATETIME"]

    def __enter__(self):
        return self

    def __exit__(self, exc_t, exc_v, trace):
        self.save()
        self.c.close()

    def CheckArgs(self, table, args):
        for k in args.keys():
            if k not in self.c.execute(f"PRAGMA table_info({table.name})").fetchone():
                raise errors.ArgumentNotFoundException(f"Column {k} from (Table {table.name}) not found.")

    def create_table(self, table: Table, **args):
        """
        Create a table (Use Table Object to warp)
        :param table: Table Object
        :param args: Containing the arguments name and type.
        :return: None
        """
        for v in args.values():
            if v not in ["NULL", *self.ints, *self.real, *self.strings, *self.numeric]:
                raise errors.TypeNotFoundException("Expected type {} but {} was found".format(["NULL", "INTEGER", "REAL", "TEXT", "BLOB"], v))
        i = []

        for k, v in args.items():
            i.append(f"{k} {v}")
        self.c.execute(f"CREATE TABLE IF NOT EXISTS {table.name} (%s)" % " ".join(i))

    def delete_table(self, table: Table):
        """
        Delete Table
        :param table: Table to be deleted.
        :return: Table name that was deleted.
        """
        self.c.execute(f"DROP TABLE IF EXISTS {table.name}")
        return table.name

    def add_record(self, table: Table, **args):
        """
        Add a record to the db
        :param table: Database to be added.
        :param args: Records
        :return: None
        """
        k = args.keys()
        v = args.values()

        self.c.execute(f"INSERT INTO {table.name} ({','.join(k)}) VALUES ({','.join(list('?' * len(k)))})", [s for s in v])
        self.save()

    def add_multiple(self, table: Table, data: list):
        """
        Adds Multiple Rows, For example:
        add_multiple(table, [["username", "password"], ["testing", "lol"]]
        :param table: Table to be inserted
        :param data: Data to be inserted.
        :return: None
        """
        try:
            data[0][0]
        except KeyError:
            raise errors.MultipleRowInsertException("The list should contain another list!")
        for d in data:
            self.c.execute(f"INSERT INTO {table.name} VALUES ({','.join(d)})")
        self.save()

    def fetch_all(self, table: Table):
        """
        Fetch all data from a table.
        :param table: Table to be executed on.
        :return: A list containing the data.
        """
        r = self.c.execute(f"SELECT * FROM {table.name}").fetchall()

        f = []
        for a in r:
            f.append(Table.Query(self, table, a))

        return f


    def fetch_data(self, table: Table, **args):
        """
        Fetch data with filter on.n
        :param table: Table to be executed on.
        :param args: Conditions / Filters.
        :return: A list containing the data which match the conditions or filter
        """
        # self.CheckArgs(table, args)

        r = []
        for k, v in args.items():
            r.append(k + "=" + f"'{v}'" if table.types_[k] in self.strings else v)

        r = self.c.execute(f"SELECT * FROM {table.name} WHERE {' AND '.join(r)}").fetchall()

        f = []
        for a in r:
            f.append(Table.Query(self, table, a))
        return f


    def update(self, table: Table, column, new_val, **filter_):
        self.CheckArgs(table, filter_)
        if len(filter_):
            k = list(filter_.keys())[0]
            v = list(filter_.values())[0]
            r = k + "=" + f"'{v}'" if table.types_[k] in self.strings else v

        e = column + "=" + f"'{new_val}'" if table.types_[column] in self.strings else new_val

        self.c.execute(f"UPDATE {table.name} SET {e} {'' if not r else 'WHERE ' + r}")
        self.save()

    def delete_record(self, table: Table, **args):
        r = []

        for k, v in args.items():
            r.append(k + "=" + f"'{v}'" if table.types_[k] in self.strings else v)

        self.c.execute(f"DELETE FROM {table.name} WHERE {' AND '.join(r)}")
        self.save()