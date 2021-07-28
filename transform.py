import pandas as pd
import numpy as np
from datetime import date
import dateparser

def standardize_date(to_date):
    to_date = dateparser.parse(to_date)
    to_date = np.datetime64(to_date).astype(date).date()
    return to_date

def std_date_day(to_date):
    to_date = dateparser.parse(to_date, settings={'DATE_ORDER': 'DMY'}).date()
    return to_date
