import numpy as np
import random
import datetime as dt
import pandas as pd
import csv
from pathlib import Path
import mysql.connector #pip install mysql-connector-python

# ======================= SEED =======================
seed = 10
np.random.seed(seed)
random.seed(seed)

# ======================= CONSTANTS =======================
creation_date = dt.date(1990, 12, 2)
minimal_wage = 4666
min_hamster_weight = 20
max_hamster_weight = 80
doping_chance = 0.03

# ======================= LOAD_IN_DATA =======================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "dane"

def load_names(filename):
    path = DATA_DIR / filename
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row["name"] for row in reader] # if you add in data make sure that the headliner of name is called name otherwise this function won't read it

first_names = load_names("first_names.csv")
last_names = load_names("last_names.csv")
companies = load_names("company_names.csv")
illegal_substances = load_names("illegal_substances.csv")


# ======================= GENERATE_DATA =======================
def generate_phone_number():
    return f"{random.randint(1, 999999999):09d}"

def generate_postal_code():
    return f"{random.randint(1,99):02d}-{random.randint(1,999):03d}"    
    
def generate_money_ammount(min_amm, max_amm):
    mean = (min_amm + max_amm) / 2
    std = (min_amm + max_amm) / 6
    
    # preserving normal distribution
    while True:
        value = np.random.normal(loc=mean, scale=std) # most values between (mean - 3*std, mean + 3*std)
        if (min_amm <= value  <= max_amm): 
            return round(value)

def generate_random_date(min_date, max_date):
    if (max_date <= min_date):
        raise ValueError("min_date has to be smaller than max_date")
    delta_days = (max_date - min_date).days
    date = min_date + dt.timedelta(days=random.randrange(delta_days))
    return date

def generate_weight(min_weight, max_weight):
    if (max_weight <= min_weight):
        raise ValueError("min_weight has to be smaller than max_weight")
    mean = (min_weight + max_weight) / 2
    std = (min_weight + max_weight) / 6
    
    # preserving normal distribution
    while True:
        weight = np.random.normal(loc=mean, scale=std) # most of values between (mean - 3*std, mean + 3*std)
        if (min_weight <= weight <= max_weight):
            return round(weight)

def check_if_positive(chance): # chance should be a value between 0-1 and represents how likely sth is to happend
    if (chance>1 or chance<0):
        raise ValueError("chance powinno należeć do [0,1]")
    if (random.random() <= chance):
        return True
    else:
        return False
    
# ======================= SQL CONNECTION =======================        
conn = mysql.connector.connect(
    host="giniewicz.it",
    user="team13",
    password="te@mzie",
    database="team13"
)

cursor = conn.cursor()


# tutaj jest przykladowa funkcja ktora wypelnia tabele n rekordami. Musimy zrobic taka funkcje dla kazdej tabeli 
def fillPracownicy(n):
    for i in range(n):
        rImie = random.choice(first_names)
        rNazwisko = random.choice(last_names)
        rNumer = generate_phone_number()
        rPostal = generate_postal_code()
        #... 
        rWynagrodzenie = minimal_wage
        cursor.execute(
            "INSERT INTO Pracownicy (imie, nazwisko, numer_telefonu, kod_pocztowy, miasto, ulica, wynagrodzenie)" \
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (rImie, rNazwisko,rNumer,rPostal,...,rWynagrodzenie)
            
        )

# def fillSponsorzy...
# ...


# i pozniej tylko
# fillPracownicy(20)
# ...


conn.commit()

cursor.close()
conn.close()       
