import pandas as pd
from db_credentials import connection, connect_engine

# BE CAREFUL WITH THIS FUNCTION, IT RESETS THE journal table
#def init_journals():
#    journals = pd.read_csv('journals.csv')
#    journals.insert(0, 'journal_id', range(len(journals.index)))
#	engine = connect_engine()
#	journals.to_sql("journal", engine, if_exists='replace', index = False)

def get_journal():
	conn = connection()
	journal = pd.read_sql_query("SELECT * FROM journal", conn)
	#Closing the connection
	conn.close()
	return journal

def most_recent_date(journal):
	conn = connection()
	cursor = conn.cursor()
	last_update = cursor.execute("""SELECT MAX(pub_date)
                                FROM article
                                WHERE source = '""" + journal + "';")
	last_update = cursor.fetchone()
	return last_update

def add_articles(articles):
	# establishing the connection
	engine = connect_engine()
	articles.to_sql("article", engine, if_exists='append', index = False)

def remove_duplicates():
	conn = connection()

	#Creating a cursor object using the cursor() method
	cursor = conn.cursor()
	cursor.execute("""DELETE a1 FROM article a1 INNER JOIN article a2 WHERE a1.article_id > a2.article_id AND a1.title = a2.title AND a1.link = a2.link;""")
	conn.commit()  # commit the changes
	print("Duplicates removed:", cursor.rowcount)
	# need to run this command to reset primary key
	cursor.execute("ALTER TABLE article DROP article_id;")
	cursor.execute("ALTER TABLE article AUTO_INCREMENT = 1;")
	cursor.execute("ALTER TABLE article ADD article_id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;")
	conn.commit()

# Check if a table exists and if not it creates it
def create_table():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS article(
        id int(11) NOT NULL auto_increment,
        title text,
        link text,
        snippet text,
        pub_date datetime NULL,
        source varchar(100) NOT NULL default '',
        PRIMARY KEY  (id)
    )""")
    conn.commit()
