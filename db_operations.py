from db_credentials import connection
import pandas as pd

# Creates articles table
def create_articles_table():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles(
        id int(11) NOT NULL auto_increment,
        title VARCHAR(255),
        pub_date date NULL,
        snippet text,
        url VARCHAR(255),
        source_id varchar(100),
		CONSTRAINT UNIQUE(title, url, source_id),
		PRIMARY KEY (id)
    );""")
    conn.commit()

def create_events_table():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id int(11) NOT NULL auto_increment,
        title VARCHAR(255),
        start_date date NULL,
        end_date date NULL,
        snippet text,
        url VARCHAR(255),
        source_id int,
		CONSTRAINT UNIQUE(title, url),
		PRIMARY KEY (id)
    );""")
    conn.commit()


# Takes as inputs the fields of each article and inserts them in a MySQL database
def insert_articles(title, pub_date, snippet, url, source_id):

	# Establishing the connection
	conn = connection()
	cursor = conn.cursor()

	# Insert query
	cursor.execute(f"""INSERT IGNORE INTO articles(title, pub_date, snippet, url, source_id)
					VALUES(%s,%s,%s,%s,%s);""", (title, pub_date, snippet, url, source_id))

	# Commit and close
	conn.commit()
	cursor.close()
	conn.close()

def insert_events(title, start_date, end_date, snippet, url, source_id):

	# Establishing the connection
	conn = connection()
	cursor = conn.cursor()

	# Insert query
	cursor.execute(f"""INSERT IGNORE INTO articles(title, pub_date, snippet, url, source_id)
					VALUES(%s,%s,%s,%s,%s);""", (title, pub_date, snippet, url, source_id))

	# Commit and close
	conn.commit()
	cursor.close()
	conn.close()


def get_newsletter_articles(date):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT title, pub_date, url, source_id FROM articles WHERE pub_date >= %s;""", (date,))
    records = pd.DataFrame(cursor.fetchall(), columns = ['title', 'pub_date', 'url', 'source'])
    cursor.close()
    conn.close()

    return records
