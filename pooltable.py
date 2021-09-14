import datetime
import os
import json

class PoolTable(object):
    def __init__(self, name, occupied = False, hour = 0, minute = 0):
        self.name = name
        self.occupied = occupied
        self.hour = hour
        self.minute = minute
    def is_occupied(self):
        return self.occupied
    def checkout(self):
        if self.occupied == False:
            self.hour = datetime.datetime.now().hour
            self.minute = datetime.datetime.now().minute
            self.occupied = True
        else:
            print('This table is already checked out')
    def checkin(self):
        if self.occupied == True:
            self.occupied = False
            print('Elapsed time: ' ),
            hour = datetime.datetime.now().hour - self.hour
            minute = datetime.datetime.now().minute - self.minute
            if hour > 0:
                print(str(hour)),
            else:
                print('00'),
            print(':'),
            if minute > 0:
                print(str(minute))
            else:
                print(str(0-minute))
            return float(hour + 0.01*minute)
        else:
            print('Table not yet occupied')
            return 0.0
    def to_dictionary(self):
        return { 'name':self.name,'occupied' : self.occupied,'hour': self.hour, 'minute': self.minute}

class Tables(object):
    def __init__(self, cost = 0.0):
        self.cost = cost
        self.tables = []
    def add_table(self, name):
        self.tables.append(PoolTable(name))
    def load(self,filename):
        with open(filename) as file_object:
            for item in json.load(file_object):
                self.tables.append(PoolTable(item['name'], item['occupied'],item['hour'],item['minute']))
    def to_dictionary(self):
        arr = []
        for item in self.tables:
            arr.append(item.to_dictionary())
        return arr
    def dump(self,filename):
        with open(filename,'w') as file_object:
            json.dump(self.to_dictionary(), file_object, sort_keys=True, indent=4)
    def view_tables(self):
        for table in self.tables:
            print('Table ' + str(table.name+1) + ' -- '),
            print('Occupied: ' + str(table.occupied)),
            if table.occupied:
                print(' -- Start time: ' + str(table.hour) + ':' + str(table.minute)),
            print('\n')
    def checkin(self,index):
        checkin = self.tables[index].checkin()
        if checkin > 0:
            return 'Cost of stay was: $' + str(checkin * self.cost )
        else:
            return ''
