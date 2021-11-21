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
        if type(lon) != int and type(lon) != float:
            raise TypeError('incorrect type. Enter a integer or float')
        if float(lon) < -180 or float(lon) > 180:
            raise Exception('latitude input is out of bounds. Latitude must be between -180 and 180')
        if type(lon) != int and type(lon) != float:
            raise TypeError('incorrect type. Enter a integer or float')
        if float(lon) < -180 or float(lon) > 180:
            raise Exception('latitude input is out of bounds. Latitude must be between -180 and 180')

        distance_list = []
        distance_list_names = []

        for i in range(len(self.glacier_init)):
            distance = haversine_distance(lat,lon,self.glacier_init[i].lat,self.glacier_init[i].lon)
            distance_list.append([self.glacier_init[i].name,distance])
        
        distance_list.sort(key=lambda sort: sort[1])
        for j in range(len(self.glacier_init)):
            distance_list_names.append(distance_list[j][0])
        print( distance_list_names[0:n])
    
    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        result_list = []
        code_list = [str(i) for i in str(code_pattern)]
        number_of_unknown = code_list.count('?')
        if type(code_pattern) != int:
            raise TypeError('incorrect type. Enter integer')
        if len(str(code_pattern)) != 3:
            raise Exception('Input of wrong length. Enter 3 digit code')
        if number_of_unknown == 0:
            code_pattern = int(code_pattern)
            for i in range(len(self.glacier_init)):
                if code_pattern == self.glacier_init[i].code:
                    result_list.append(self.glacier_init[i].name)
        elif number_of_unknown == 1:
            for i in range(2):
                if code_list[0] == '?':
                    for j in range(len(self.glacier_init)):
                        code_list_comparrison = [str(k) for k in str(self.glacier_init[j].code)]
                        if code_pattern[1] == code_list_comparrison[1] and code_pattern[2] == code_list_comparrison[2]:
                            result_list.append(self.glacier_init[j].name)
                if code_list[1] == '?':
                    for j in range(len(self.glacier_init)):
                        code_list_comparrison = [str(k) for k in str(self.glacier_init[j].code)]
                        if code_pattern[0] == code_list_comparrison[0] and code_pattern[2] == code_list_comparrison[2]:
                            result_list.append(self.glacier_init[j].name)
                if code_list[2] == '?':
                    for j in range(len(self.glacier_init)):
                        code_list_comparrison = [str(k) for k in str(self.glacier_init[j].code)]
                        if code_pattern[1] == code_list_comparrison[1] and code_pattern[0] == code_list_comparrison[0]:
                            result_list.append(self.glacier_init[j].name)
        elif number_of_unknown == 2:
            for i in range(2):
                if code_list[0] == '?' and code_list[1] == '?':
                    for j in range(len(self.glacier_init)):
                        code_list_comparrison = [str(k) for k in str(self.glacier_init[j].code)]
                        if code_pattern[2] == code_list_comparrison[2]:
                            result_list.append(self.glacier_init[j].name)
                if code_list[0] == '?'and code_list[2] == '?':
                    for j in range(len(self.glacier_init)):
                        code_list_comparrison = [str(k) for k in str(self.glacier_init[j].code)]
                        if code_pattern[1] == code_list_comparrison[1]:
                            result_list.append(self.glacier_init[j].name)
                if code_list[1] == '?'and code_list[2] == '?':
                    for j in range(len(self.glacier_init)):
                        code_list_comparrison = [str(k) for k in str(self.glacier_init[j].code)]
                        if code_pattern[0] == code_list_comparrison[0]:
                            result_list.append(self.glacier_init[j].name)
        elif number_of_unknown == 3:
           for i in range(len(self.glacier_init)):
                result_list.append(self.glacier_init[i].name)
        print(result_list)


    def sort_by_latest_mass_balance(self, reverse, n=5):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        for j in range(len(self.glacier_init)):
            if len(self.glacier_init[j].year_balance_dict.keys()) == 0:
                continue
            else:
                keys = self.glacier_init[j].year_balance_dict.keys()
                values = self.glacier_init[j].year_balance_dict.values()
                self.latest_year_measurment.append([j,max(zip(keys, values))])
            self.latest_year_measurment.sort(key=lambda sort:sort[1][1])
        for i in range(len(self.latest_year_measurment)):
            dummy = self.latest_year_measurment[i][0]
            self.sorted_glaciers.append(self.glacier_init[dummy])

        if reverse == False:
            return self.sorted_glaciers[0:n]
        elif reverse == True:
            return self.sorted_glaciers[-n:]


    def summary(self):
        print("This collection has", str(len(self.glacier_init)), "glaciers")
        print("The earliest measurement was in", str(min(self.year)))
        negative_count = 0
        positive_count = 0
        for i in range(len(self.latest_year_measurment)):
            if self.latest_year_measurment[i][1][1] < 0 :
                negative_count += 1
            elif self.latest_year_measurment[i][1][1] > 0:
                positive_count += 1
        print(str(int((negative_count/(positive_count+negative_count))*100))+"%" ,"of the glaciers shrunk in their last measurement")

    def plot_extremes(self, output_path):
        raise NotImplementedError
