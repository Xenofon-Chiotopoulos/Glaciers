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
        raise NotImplementedError

    def plot_mass_balance(self, output_path):
        raise NotImplementedError

        
class GlacierCollection:

    def __init__(self, file_path):
        raise NotImplementedError

    def read_mass_balance_data(self, file_path):
        raise NotImplementedError

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
