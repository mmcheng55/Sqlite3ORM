from .__init__ import Database


class Table:
    __slots__ = ["db", "name", "types_"]

    def __init__(self, db: Database, name, **args):
        """
        Table Object
        :param db: Database
        :param name: Table Name
        :param args: Table Objects.
        """
        self.db = db
        self.name = name

        self.types_ = args

        self.db.create_table(self, **args)

    def delete_table(self):
        self.db.delete_table(self)

    def delete(self, **args):                       return self.db.delete_record(self, **args)

    def fetch(self, **args):                        return self.db.fetch_data(self, **args)

    def update(self, column, new_val, **args):      return self.db.update(self, column, new_val, **args)

    def add(self, **data):                          return self.db.add_record(self, **data)

    def add_multiple(self, data):                   return self.db.add_multiple(self, data)


class Query(object):
    def __init__(self, db: Database, table: Table, result: tuple):
        """
        Query Object
        :param db: Database
        :param table: Table
        :param result: Fetched Data
        """
        self.db = db
        self.database = self.db

        self.table = table

        self.raw = {}
        for i in result:
            self.raw.update({list(self.table.types_.keys())[result.index(i)]: i})

        for i in result:
            self.__setattr__(list(self.table.types_.keys())[result.index(i)], i)
