import pandas as pd
from datetime import date, timedelta
df = pd.read_csv('newsletter.csv')

days = timedelta(7)

df['pub_date'] = pd.to_datetime(df["pub_date"])
df['pub_date'] = df['pub_date'].dt.date

start = today-days
end = date.today()
df = df[(df['pub_date'] >= start) & (df['pub_date'] <= end)]
df.to_csv('newsletter2.csv', index = False)
