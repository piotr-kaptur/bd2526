import numpy as np
import random
import datetime as dt

seed = 10
np.random.seed(seed)
random.seed(seed)
creation_date = dt.date(1990, 12, 2)


def generate_phone_number():
    return f"{random.randint(1, 999999999):09d}"

def generate_postal_code():
    return f"{random.randint(1,99):02d}-{random.randint(1,999):03d}"    
    
def generate_money_ammount(min_amm, max_amm):
    return random.randint(min_amm, max_amm)

def generate_random_date(min_date, max_date):
    if (max_date <= min_date):
        raise ValueError("start_days has to be smaller than end date")
    delta_days = (max_date - min_date).days
    date = min_date + dt.timedelta(days=random.randrange(delta_days))
    return date

def generate_hamster_weight():
    weight = max(20, min(np.random.normal(loc=50, scale=9), 80)) # most of values between (23, 77)
    return weight

def check_if_positive(chance):
    # chance should be a value between 0-1 and represents how likely sth is to happend
    if chance>1 or chance<0:
        raise ValueError("chance powinno należeć do [0,1]")
    if (random.random() <= chance):
        return True
    else:
        return False
        
