import pytest
import glaciers
import csv
from math import dist
from pathlib import Path
from typing import Collection
from utils import haversine_distance
from datetime import datetime
import matplotlib.pyplot as plt
from utils import haversine_distance


location = ''
file_path_A = Path(location + "sheet-A.csv")
file_path_EE = Path(location + "sheet-EE.csv")

def test_read_mass_balance():
    collection = glaciers.GlacierCollection(file_path_A)
    collection.read_mass_balance_data(file_path_EE)
    
    #this specific glacier has partial and full year measurements therefore we also check the add_mass_balance_method
    assert collection.glacier_init[0].year_balance_dict == {2015: -793, 2016: -418, 2017: 332, 2018: -7886, 2019: -2397, 2020: -13331}
    assert collection.glacier_init[4].year_balance_dict == {2018: -2602, 2019: -3308}
    #Checking mass balance works for glaciers with no measurments
    assert collection.glacier_init[1].year_balance_dict == {}


def test_filter_by_code():
    collection = glaciers.GlacierCollection(file_path_A)
    collection.read_mass_balance_data(file_path_EE)
    #checking complete code
    assert collection.filter_by_code(534) == ['ALERCE', 'PIEDRAS BLANCAS', 'ARTESONRAJU']
    #checking incomplete code
    assert collection.filter_by_code('5?5') == ['PENON', 'PENON']
    #checking incomplete code
    assert collection.filter_by_code('??2') == ['MEOLA', 'FLAAJOKULL', 'FLAAJOKULL E 146', 'FLAAJOKULL E 148', 'FLAAJOKULL E 150', 'MULAJOKULL S', 'OLDUFELLSJOKULL', 'SIDUJOKULL E M 175', 'SIDUJOKULL E M 177', 'SKEIDARARJOKULL E1', 'SKEIDARARJOKULL E2', 'SKEIDARARJOKULL E3', 'SKEIDARARJOKULL W', 'MEOLA', 'FLAAJOKULL', 'FLAAJOKULL E 146', 'FLAAJOKULL E 148', 'FLAAJOKULL E 150', 'MULAJOKULL S', 'OLDUFELLSJOKULL', 'SIDUJOKULL E M 175', 'SIDUJOKULL E M 177', 'SKEIDARARJOKULL E1', 'SKEIDARARJOKULL E2', 'SKEIDARARJOKULL E3', 'SKEIDARARJOKULL W']

def test_sort_by_latest_mass_balance():
    collection = glaciers.GlacierCollection(file_path_A)
    collection.read_mass_balance_data(file_path_EE)

    assert collection.sort_by_latest_mass_balance(True,1)[0].glacier_id == '03292'
    assert collection.sort_by_latest_mass_balance(False,1)[0].glacier_id == '01329'

#Negative tests

def test_galcier_init_id():
    ##ID_GLACIER
    #Negative test for wrong input type
    with pytest.raises(TypeError, match = ('incorrect type. Enter a string')):
        glaciers.Glacier(999,'AGUA NEGRA', 'AR',-30.16490,-69.80940, '638')
    #Negative test for wrong input length
    with pytest.raises(ValueError, match = ('Id not appropriate length. Enter a string of length 5')):
        glaciers.Glacier('012','AGUA NEGRA', 'AR',-30.16490,-69.80940, '638')

def test_galcier_init_name():
    #NAME 
    #Negative test for wrong input type
    with pytest.raises(TypeError, match = ('incorrect type. Enter a string')):
        glaciers.Glacier('04532',2222, 'AR',-30.16490,-69.80940, '638')
    
def test_galcier_init_unit():
    #UNIT
    #Negative test for wrong input type
    with pytest.raises(TypeError, match = ('incorrect type. Enter a string')):
        glaciers.Glacier('04532','AGUA NEGRA', 999,-30.16490,-69.80940, '638')
    #Negative test for unit length
    with pytest.raises(ValueError, match=('unit not appropriate length. Enter a string of length 2')):
        glaciers.Glacier('04532','AGUA NEGRA', 'ARR',-30.16490,-69.80940, '638')
    
    

