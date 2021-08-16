from db_operations import *

df = get_newsletter_articles('2021-08-10')
df.to_csv('newsletter.csv')
