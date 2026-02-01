import numpy as np
import random
import datetime as dt
import pandas as pd
import csv
from pathlib import Path
import math
import mysql.connector #pip install mysql-connector-python

# ======================= SEED =======================
seed = 10
np.random.seed(seed)
random.seed(seed)

# ======================= CONSTANTS =======================
creation_date = dt.date(1990, 12, 2)
current_date = dt.date.today()

# HAMSTERS
hamster_ammount = 1000
min_hamster_weight = 20
max_hamster_weight = 80
min_hamster_height = 4
max_hamster_height = 10
hamster_death_chance = 0.03
hamster_races = ["syryjski","dzungarski","roborowski","chinski","campbella",
               "europejski","gansu","mongolski","turecki","rumunski"]
hamster_colours = ["perlowy","karmelowy","grafitowy","piaskowy","popielaty",
                   "czekoladowy","miodowy","srebrzysty","waniliowy","szampanski"]
hamster_runner_percentage = 0.8

# FINANCES
min_finance_money = 100000  #100,000
max_finance_money = 1000000 #1,000,000

# FORMULAS
racing_formulas = [
    ("Slalom tunelowy", "jazda"),
    ("Wyscig kolowy", "jazda"),
    ("Sprint prosty", "bieg"),
    ("Bieg z przeszkodami", "bieg"),
    ("Bieg po trocinach", "bieg")
]

# COMPETTION
competition_ammount = 100
tests_per_competition_ammount = hamster_ammount/100

# WORKERS
minimal_wage = 4666
maximum_wage = 15462





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
    std = (max_amm - min_amm) / 6
    
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

def generate_hamster_death_date(birth_date):
    two_years = dt.timedelta(days = 2*365)
    three_years = dt.timedelta(days = 3*365)
    if (random.random() < hamster_death_chance):
            return generate_random_date(birth_date, min(
                birth_date + two_years, current_date))
    if (current_date - birth_date > two_years):
            return  generate_random_date(birth_date + two_years,min(
                                        birth_date + three_years, current_date))
    return None
    

def generate_weight(min_weight, max_weight):
    if (max_weight <= min_weight):
        raise ValueError("min_weight has to be smaller than max_weight")
    mean = (min_weight + max_weight) / 2
    std = (max_weight -  min_weight) / 6
    
    # preserving normal distribution
    while True:
        weight = np.random.normal(loc=mean, scale=std) # most of values between (mean - 3*std, mean + 3*std)
        if (min_weight <= weight <= max_weight):
            return round(weight)
        
def generate_height(min_height, max_height):
    if (max_height <= min_height):
        raise ValueError("min_height has to be smaller than max_height")
    mean = (min_height + max_height) / 2
    std = (max_height - min_height) / 6
    
    # preserving normal distribution
    while True:
        weight = np.random.normal(loc=mean, scale=std) # most of values between (mean - 3*std, mean + 3*std)
        if (min_height <= weight <= max_height):
            return round(weight)

def check_if_positive(chance): # chance should be a value between 0-1 and represents how likely sth is to happend
    if (chance>1 or chance<0):
        raise ValueError("chance powinno należeć do [0,1]")
    if (random.random() <= chance):
        return True
    else:
        return False

def generate_racing_formula(percentage_of_runners):
    if (random.random() < percentage_of_runners):
        return "bieg"
    return "jazda"
    
# ======================= SQL CONNECTION =======================        
conn = mysql.connector.connect(
    host="giniewicz.it",
    user="team13",
    password="te@mzie",
    database="team13"
)

cursor = conn.cursor()

def fill_chomiki(n):
    for _ in range(n):
        imie = random.choice(first_names)
        rasa = random.choice(hamster_races)
        kolor = random.choice(hamster_colours)
        waga = generate_weight(min_hamster_weight, max_hamster_weight)
        wzrost = generate_height(min_hamster_height, max_hamster_height)
        plec = random.choice(['M','F'])
        data_urodzenia = generate_random_date(creation_date, current_date)
        data_smierci = generate_hamster_death_date(data_urodzenia)          
        
        cursor.execute(
            """INSERT INTO chomiki (imie,rasa,kolor,waga,wzrost,plec,
            data_urodzenia,data_smierci)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (imie, rasa, kolor, waga, wzrost, plec, data_urodzenia, data_smierci))

def fill_finansowanie(n):
    for _ in range(n):
        zrodlo = None # ktoś musi csv zrobic z tym
        kwota = generate_money_ammount(min_finance_money, max_finance_money)
        data_finansowania = generate_random_date(creation_date, current_date)
        
        cursor.execute(
            """INSERT INTO finansowanie (zrodlo,kwota,data_finansowania)
            VALUES (%s, %s, %s)""",
            (zrodlo, kwota, data_finansowania))

def fill_konkurencje():
    for name, formula in racing_formulas:
        nazwa_konkurencji = name
        formula = formula
        
        cursor.execute(
            """INSERT INTO finansowanie (nazwa_konkurencji, formula)
            VALUES (%s, %s)""",
            (nazwa_konkurencji, formula))

def fill_kontrole(n):
    #probelmatyczne (duzo relacji)
    for i in range (1, competition_ammount*tests_per_competition_ammount):
        id_zawodow = math.ceil(i/tests_per_competition_ammount)
        pass
    
def fill_pracownicy(n):
    #problematyczne (relacja miasto->ulica->kod_pocztowy)
    for _ in range(n):
        imie = random.choice(first_names)
        nazwisko = random.choice(last_names)
        numer_telefonu = generate_phone_number()
        #to trzeba wyjac z bazydanych cities1500 upewnic sie ze ulica jest w miescie
        # kod pocztowy zwiazany z miastem pozdro kaptur
        miasto = None
        ulica = None
        kod_pocztowy = None 
        wynagrodzenie = generate_money_ammount(minimal_wage, maximum_wage)
        
        cursor.execute(
            """INSERT INTO pracownicy (imie, nazwisko, numer_telefonu, kod_pocztowy, 
            miasto, ulica, wynagrodzenie)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (imie, nazwisko, numer_telefonu, kod_pocztowy, miasto, ulica, 
             wynagrodzenie))

def fill_sponsorzy():
    for company in companies:
        nazwa_firmy = company
        numer_telefonu = generate_phone_number()
        
        cursor.execute(
            """INSERT INTO pracownicy (nazwa_firmy, numer_telefonu)
            VALUES (%s, %s)""",
            (nazwa_firmy, numer_telefonu))

def fill_sponsorzy_umowy():
    # w chuj roboty
    pass

def fill_substancje_zakazane():
    for substance in illegal_substances:
        nazwa = substance
        
        cursor.execute(
            """INSERT INTO pracownicy (nazwa)
            VALUES (%s)""",
            (nazwa))

def fill_wyniki_kontroli():
    # trudne ale nie tak bardzo jak inne
    pass

def fill_wyniki_zawodow()
    #to po zawodach
    pass

def fill_zawody():
    #next
    pass

        

        
    
    
    





# def fillSponsorzy...
# ...


# i pozniej tylko
# fillPracownicy(20)
# ...


conn.commit()

cursor.close()
conn.close()       
