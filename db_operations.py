import pandas as pd
from db_credentials import connection
import re

# Check if a table exists and if not it creates it
def create_table():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles(
        id int(11) NOT NULL auto_increment,
        title VARCHAR(255),
        pub_date date NULL,
        snippet text,
        url VARCHAR(255),
		CONSTRAINT UNIQUE(title, url),
		PRIMARY KEY (id)
    );""")
    conn.commit()


def insert_articles(title, pub_date, snippet, url):
	## I need to escape single quotes
	#snippet = re.sub(snippet, "'", "''")
	# Establishing the connection
	conn = connection()
	#title = conn.escape_string(title)

	cursor = conn.cursor()
	cursor.execute(f"""INSERT IGNORE INTO articles(title, pub_date, snippet, url)
					VALUES(%s,%s,%s,%s);""", (title, pub_date, snippet, url))
	conn.commit()
	cursor.close()
	conn.close()
