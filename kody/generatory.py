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
hamster_ammount = 10000 # 10,000
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
min_finance_money = 1e5  #100,000
max_finance_money = 1e6 #1,000,000
min_sponsor_deal_cash_amm = 1e4 # 10,000
max_sponsor_deal_cash_amm = 5*1e5 # 500,000

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
tests_per_competition_ammount = int(hamster_ammount/1000)
min_prize_pool = 1e5 # 100,000
max_prize_pool = 1e6 #1,000,000

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
competiton_names = load_names("competition_names.csv")
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
cursor1 = conn.cursor()
cursor2 = conn.cursor()

def generate_tables():
    cursor.execute(
    "CALL generate_tables()")

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
        zrodlo = None # ktoś musi csv zrobic z tym, mi juz wystarczy
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

def fill_kontrole():
    sql1 ="""
    SELECT id_zawodow, data_zawodow 
    FROM zawody
    ORDER BY id_zawodow
    """
    cursor1.execute(sql1)
    for id_zawodow, data_zawodow in cursor1:
        
        cursor2.execute("""SELECT id_chomika
        FROM wyniki_zawodow
        WHERE id_zawodow = %s
        """, (id_zawodow,))
        chomiki = [row[0] for row in cursor2.fetchall()]
        k = min(tests_per_competition_ammount, len(chomiki))
        chosen_hamsters = random.sample(chomiki, k)
        for hamster in chosen_hamsters:
            id_zawodow = id_zawodow
            id_chomika = hamster
            data_kontroli = data_zawodow
            wynik_kontroli = check_if_positive(doping_chance)
            
            cursor.execute(
            """INSERT INTO kontrole (id_zawodow, id_chomika, data_kontroli, 
            wynik_kontroli)
            VALUES (%s, %s, %s, %s)""",
            (id_zawodow, id_chomika, data_kontroli, wynik_kontroli))
            
            
            
    
def fill_pracownicy(n):
    #problematyczne (relacja miasto->ulica->kod_pocztowy)
    for _ in range(n):
        imie = random.choice(first_names)
        nazwisko = random.choice(last_names)
        numer_telefonu = generate_phone_number()
        miasto = random.choice(city_names)
        kod_pocztowy = None # usunalem to, jezeli nie chcecie tego usuwac czytaj: to sobie to robcie moj pomysl byl taki ze generuje za kazdym razem csv ktore kazdemu miastu przypisuje unikalny randomowo wygenerowany kod-pocztowy po czym przy tworzeniu po prostu odczytujemy z krotki/csv
        wynagrodzenie = normal_distribution(minimal_wage, maximum_wage)
        
        cursor.execute(
            """INSERT INTO pracownicy (imie, nazwisko, numer_telefonu, miasto, 
            ulica, wynagrodzenie)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (imie, nazwisko, numer_telefonu, miasto, wynagrodzenie))

def fill_sponsorzy():
    for company in companies:
        nazwa_firmy = company
        numer_telefonu = generate_phone_number()
        
        cursor.execute(
            """INSERT INTO sponsorzy (nazwa_firmy, numer_telefonu)
            VALUES (%s, %s)""",
            (nazwa_firmy, numer_telefonu))

def fill_sponsorzy_umowy(n):
    sql1 = """
    SELECT id_sponsora
    FROM SPONSORZY"""
    cursor1.execute(sql1)
    
    sql2 ="""
    SELECT id_chomika, data_urodzenia, data_smierci
    FROM chomiki"""
    cursor2.execute(sql2)
    
    sponsors_id = [row[0] for row in cursor1.fetchall()]
    chomiki_info = cursor2.fetchall() # to bedzie w chuj wolne ale nw jak inaczej to zrobic
    
    for _ in range(n):
        id_sponsora = random.choice(sponsors_id)
        id_chomika, data_urodzenia, data_smierci = random.choice(chomiki_info)
        if data_smierci is None:
            data_smierci = current_date
        rozpoczecie_umowy = generate_random_date(data_urodzenia, data_smierci)
        koniec_umowy =  generate_random_date(rozpoczecie_umowy, data_smierci)
        kwota = normal_distribution(min_sponsor_deal_cash_amm, 
                                    max_sponsor_deal_cash_amm)
        cursor.execute(
            """INSERT INTO sponsorzy_umowy (id_sponsora, id_chomika, rozpoczecie_umowy, 
            koniec_umowy, kwota)
            VALUES (%s, %s, %s, %s, %s)""",
            (id_sponsora, id_chomika, rozpoczecie_umowy, koniec_umowy, kwota))
        
        
    

def fill_substancje_zakazane():
    for substance in illegal_substances:
        nazwa = substance
        
        cursor.execute(
            """INSERT INTO substancje_zakazane (nazwa)
            VALUES (%s)""",
            (nazwa,))

def fill_wyniki_kontroli():
    sql = """
    SELECT id_kontroli
    FROM kontrole
    WHERE wynik_kontroli IS TRUE
    """
    cursor.execute(sql)
    #tutaj sortujemy tylko kontrole w których wykryto substancje
    ids = [row[0] for row in cursor.fetchall()]
    
    for control_id in ids:
        id_kontroli = control_id
        zakazane_substancje = random.choice(illegal_substances)
        cursor.execute(
            """INSERT INTO wyniki_kontroli (id_kontroli, zakazane_substancje)
            VALUES (%s, %s)""",
            (id_kontroli, zakazane_substancje))
        
    

def fill_wyniki_zawodow():
    sql = """
    SELECT z.id_zawodow AS competition_id, c.id_chomika AS hamster_id
    FROM zawody z 
    JOIN chomiki c
    ON c.data_urodzenia <= z.data_zawodow
    AND (c.data_smierci IS NULL OR c.data_smierci >= z.data_zawodow)
    ORDER BY z.id_zawodow
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
            (id_konkurencji, nazwa, data_zawodow, lokalizacja, pula_nagrod))

        

        
    
    
    





# def fillSponsorzy...
# ...


# i pozniej tylko
# fillPracownicy(20)
# ...


conn.commit()

cursor.close()
conn.close()       
