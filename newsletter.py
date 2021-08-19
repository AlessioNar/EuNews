from db_operations import *

df = get_newsletter_articles('2021-08-09')
df['section'] = 'todo'
df.to_csv('newsletter.csv', index = False)
