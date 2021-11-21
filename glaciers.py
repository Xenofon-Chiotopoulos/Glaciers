import csv
from math import dist
from pathlib import Path
from typing import Collection
from utils import haversine_distance
from datetime import datetime
import matplotlib.pyplot as plt

location = ''
file_path_A = Path(location + "sheet-A.csv")
file_path_EE = Path(location + "sheet-EE.csv")

class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):
        self.glacier_id = glacier_id
        if type(glacier_id) != str:
            raise TypeError('incorrect type. Enter a string')
        if len(glacier_id) != 5:
            raise Exception('Id not appropriate length. Enter a string of length 5')

        self.name = name
        if type(name) != str:
            raise TypeError('incorrect type. Enter a string')

        self.unit = unit
        if type(unit) != str:
            raise TypeError('incorrect type. Enter a string')
        if len(unit) != 2:
            raise Exception('Id not appropriate length. Enter a string of length 2')

        self.lat = lat
        if type(lat) != int and type(lat) != float:
            raise TypeError('incorrect type. Enter a integer or float')
        if float(lat) < -90 or float(lat) > 90:
            raise ValueError('latitude input is out of bounds. Latitude must be between -90 and 90')

        self.lon = lon
        if type(lon) != int and type(lon) != float:
            raise TypeError('incorrect type. Enter a integer or float')
        if float(lon) < -180 or float(lon) > 180:
            raise ValueError('latitude input is out of bounds. Latitude must be between -180 and 180')

        self.code = code
        if len(str(code)) != 3:
            raise Exception('Input of wrong length. Enter 3 digit code')

        self.current_year_balance = 0
        self.year = []
        self.mass_balance = []
        self.year_balance_dict = {}

    def add_mass_balance_measurement(self, year, mass_balance):
        if mass_balance[1] == True and self.current_year_balance != 0: #partical measurments fin
            self.year_balance_dict.update({year:self.current_year_balance})
            self.current_year_balance = 0
        elif mass_balance[1] == False: # partial measurments 
            self.current_year_balance += mass_balance[0]
        else:
            self.year_balance_dict.update({year:mass_balance[0]})

    def plot_mass_balance(self, output_path):
        raise NotImplementedError

        
class GlacierCollection:

    def __init__(self, file_path):
        glacier_init = []
        self.glacier_init = glacier_init
        self.year = []
        mass_balance = []
        self.mass_balance = mass_balance
        self.sorted_glaciers = []
        self.latest_year_measurment = []
        self.id_list = []

        with open(file_path_A, newline='', encoding = 'utf8') as csvfile:
            glaciers = csv.DictReader(csvfile, delimiter=',')
            for row in glaciers:
                unit = str(row['POLITICAL_UNIT']) 
                name = str(row['NAME'])
                code = int(str(row['PRIM_CLASSIFIC']) + str(row['FORM']) + str(row['FRONTAL_CHARS']))
                latitude = float(row['LATITUDE'])
                longitude = float(row['LONGITUDE'])
                id = str(row['WGMS_ID'])
        
                self.glacier_init.append(Glacier(id,name,unit,latitude,longitude,code))
                self.id_list.append(id)

    def read_mass_balance_data(self, file_path):
        with open(file_path_EE, newline='', encoding='utf8') as csvfile:
            glaciers = csv.DictReader(csvfile, delimiter = ',')
            current_glacier = 0
            for row in glaciers:
                if row['ANNUAL_BALANCE'] == '':
                    continue
                yer = int(row['YEAR'])
                if yer > datetime.now().year:
                    raise Exception('Year read from csv is in the future')
                self.year.append(yer)
                id_EE = str(row['WGMS_ID'])
                if id_EE not in self.id_list:
                    raise Exception('Unrecognised glacier encountered. All id from datasheet must correspond to a previously defined object')
                for j in range(len(self.glacier_init)):
                    if self.glacier_init[j].glacier_id == id_EE:
                        current_glacier = j
                upper_bound = int(row['UPPER_BOUND']) 
                annual_balance = row['ANNUAL_BALANCE']
                if type(annual_balance) != int and type(annual_balance) != float:
                    raise TypeError('Value entered must be a integer or float')
                annual_balance = int(annual_balance)
                if upper_bound == 9999:
                    self.glacier_init[current_glacier].add_mass_balance_measurement(yer, [annual_balance, True])
                else:
                    self.glacier_init[current_glacier].add_mass_balance_measurement(yer, [annual_balance, False])


    def find_nearest(self, lat, lon, n):
        """Get the n glaciers closest to the given coordinates."""
        raise NotImplementedError
    
    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        raise NotImplementedError

    def sort_by_latest_mass_balance(self, n, reverse):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        raise NotImplementedError

    def summary(self):
        raise NotImplementedError

    def plot_extremes(self, output_path):
        raise NotImplementedError
