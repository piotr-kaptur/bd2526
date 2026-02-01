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
competition_types_ids =[]
competition_ammount = 100
tests_per_competition_ammount = hamster_ammount/100
min_prize_pool = 10000
max_prize_pool = 500000

# RACES
min_race_time = 15
max_race_time = 30

# WORKERS
minimal_wage = 4666
maximum_wage = 15462

# ILLEGAL SUBSTANCES
doping_chance = 0.03

# ======================= LOAD_IN_DATA =======================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "dane"

def load_names(filename):
    path = DATA_DIR / filename
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row["name"] for row in reader] # if you add in data make sure that the headliner of name is called name otherwise this function won't read it

def load_cities(filename):
    path = DATA_DIR / filename
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row["City"] for row in reader]
    
first_names = load_names("first_names.csv")
last_names = load_names("last_names.csv")
companies = load_names("company_names.csv")
illegal_substances = load_names("illegal_substances.csv")
competiton_names = load_names("competiton_names.csv")
city_names = load_cities("cities.csv")


# ======================= GENERATE_DATA =======================
def normal_distribution(min_val, max_val):
    if max_val <=min_val:
        raise ValueError("min_val has to be smaller than max_val")
    mean = (min_val + max_val) / 2
    std = (max_val - min_val) / 6
    
    # preserving normal distribution
    while True:
        value = np.random.normal(loc=mean, scale=std) # most values between (mean - 3*std, mean + 3*std)
        if (min_val <= value  <= max_val): 
            return value

def generate_phone_number():
    return f"{random.randint(1, 999999999):09d}"

def generate_postal_code():
    return f"{random.randint(1,99):02d}-{random.randint(1,999):03d}"    

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
        waga = normal_distribution(min_hamster_weight, max_hamster_weight)
        wzrost = normal_distribution(min_hamster_height, max_hamster_height)
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
        kwota = normal_distribution(min_finance_money, max_finance_money)
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
            """INSERT INTO konkurencje (nazwa_konkurencji, formula)
            VALUES (%s, %s)""",
            (nazwa_konkurencji, formula))
        competition_types_ids.append(cursor.lastrowid)

def fill_kontrole(n):
    #probelmatyczne (duzo relacji)
    sql ="""
    
    """
    cursor.execute(sql)
    
def fill_pracownicy(n):
    #problematyczne (relacja miasto->ulica->kod_pocztowy)
    for _ in range(n):
        imie = random.choice(first_names)
        nazwisko = random.choice(last_names)
        numer_telefonu = generate_phone_number()
        miasto = random.choice(city_names)
        kod_pocztowy = None # ja bym to wyjebal
        wynagrodzenie = normal_distribution(minimal_wage, maximum_wage)
        
        cursor.execute(
            """INSERT INTO pracownicy (imie, nazwisko, numer_telefonu, kod_pocztowy, 
            miasto, ulica, wynagrodzenie)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (imie, nazwisko, numer_telefonu, kod_pocztowy, miasto, wynagrodzenie))

def fill_sponsorzy():
    for company in companies:
        nazwa_firmy = company
        numer_telefonu = generate_phone_number()
        
        cursor.execute(
            """INSERT INTO sponsorzy (nazwa_firmy, numer_telefonu)
            VALUES (%s, %s)""",
            (nazwa_firmy, numer_telefonu))

def fill_sponsorzy_umowy():
    # w chuj roboty
    pass

def fill_substancje_zakazane():
    for substance in illegal_substances:
        nazwa = substance
        
        cursor.execute(
            """INSERT INTO substancje_zakazane (nazwa)
            VALUES (%s)""",
            (nazwa))

def fill_wyniki_kontroli():
    sql = """
    SELECT id_kontroli
    FROM kontrole
    WHERE wynik_kontroli IS TRUE
    """
    cursor.execute(sql)
    for control_id in cursor:
        id_kontroli = control_id
        id_substancji = random.choice(illegal_substances)
        cursor.execute(
            """INSERT INTO wyniki_kontroli (id_kontroli, id_substancji)
            VALUES (%s, %s)""",
            (id_kontroli, id_substancji))
        
    

def fill_wyniki_zawodow():
    sql = """
    SELECT z.id_chomika AS competition_id, c.id_zawodow AS hamster_id
    FROM zawody z 
    JOIN chomik c
    ON c.data_urodzenia <= z.data_zawodow
    AND (c.data_smierci IS NULL OR c.data_smierci < z.data.zawodow)
    ORDER BY z.id
    """
    cursor.execute(sql)
    #tutaj sortujemy tylko chomiki które zyją
    
    for competition_id, hamster_id in cursor:
        id_zawodow = competition_id
        id_chomika = hamster_id
        czas = normal_distribution(min_race_time, max_race_time)
        
        cursor.execute(
            """INSERT INTO wyniki_zawodow (id_zawodow, id_chomika, czas)
            VALUES (%s, %s, %s)""",
            (id_zawodow, id_chomika, czas))
            

def fill_zawody(n):
    for _ in range(n):
        id_konkurencji = random.choice(competition_types_ids)
        nazwa = random.choice(competiton_names)
        data_zawodow = generate_random_date(creation_date, current_date)
        lokalizacja = random.choice(city_names)
        pula_nagrod = normal_distribution(min_prize_pool, max_prize_pool)
        
        cursor.execute(
            """INSERT INTO zawody (id_konkurencji, nazwa, data_zawodow, lokalizacja, 
            pula_nagrod)
            VALUES (%s, %s ,%s, %s, %s)""",
            (id_konkurencji, data_zawodow, nazwa, lokalizacja, pula_nagrod))

        

        
    
    
    





# def fillSponsorzy...
# ...


# i pozniej tylko
# fillPracownicy(20)
# ...


conn.commit()

cursor.close()
conn.close()       
