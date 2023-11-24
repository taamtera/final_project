import csv, os, copy

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
class DB:
    def __init__(self):
        self.database = []
        
    def load(self, csv_file_name):
        table_name = csv_file_name.split('.')[0]
        table = []
        with open(os.path.join(__location__, csv_file_name)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                table.append(dict(r))
        self.upsert(Table(table_name, table))
        return self
    
    def write(self, csv_file_name):
        table = self.select(csv_file_name.split('.')[0])
        if table.table.__len__() > 0:
            # with open(os.path.join(__location__, csv_file_name), 'w', newline='') as f:
            with open(os.path.join(__location__, csv_file_name),'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=table.table[0].keys())
                writer.writeheader()
                for row in table.table:
                    writer.writerow(row)
        return self

    def upsert(self, table):
        if self.select(table.table_name) is not None:
            self.drop(table.table_name)
        self.database.append(table)
        return self

    def join(self , table1_name, table2_name, common_key):
        table1 = self.select(table1_name)
        table2 = self.select(table2_name)
        if table1 is not None and table2 is not None:
            self.upsert(table1.join(table2, common_key))
        return self
    
    def drop(self, table_name):
        table = self.select(table_name)
        if table is not None:
            self.database.remove(table)
        return self

    def select(self, table_name, where=None, columns=None):
        for table in self.database:
            if table.table_name == table_name:
                if where is not None:
                    table = table.filter(lambda item: all(item[key].lower() == where[key] for key in where))
                if table is not None and columns is not None:
                    table = table.select(columns)
                return table
        return None

    def __str__(self) -> str:
        tbnames = []
        for table in self.database:
            tbnames.append(table.table_name)
        return str(tbnames)
    
    def print(self):
        print(self)
        return self
    
class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table
    
    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table
    
    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        if len(filtered_table.table) == 0:
            return None
        return filtered_table

    def __is_float(self, element):
        if element is None: 
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)
    
    def select(self, attributes_list):
        temps = Temps()
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps
    
    def upsert(self, data, where=None):
        if where is None:
            if self.table.__len__() == 1:
                self.table[0].update(data)
            else:
                self.table.append(data)
        else:
            for item in self.table:
                if all(item[key] == where[key] for key in where):
                    item.update(data)
        return self
    
    def drop(self, where=None):
        if where is None:
            self.table = []
        else:
            for item in self.table:
                if all(item[key] == where[key] for key in where):
                    self.table.remove(item)
        return self

    def __str__(self):
        return self.table_name + ':' + str(self.table)
    
    def __len__(self):
        return self.table.__len__()
    
    def print(self):
        for item in self.table:
            print(item)
        return self

class Temps:
    def __init__(self):
        self.temps = []
        
    def append(self, item):
        self.temps.append(item)
        return self
    
    def print(self):
        for item in self.temps:
            print(item)
        return self
    
    def __str__(self):
        return str(self.temps)