#!/bin/bash
#date=$(date '+%Y-%m-%d')

# print current date directly
#echo $(date '+%Y-%m-%d')

python scrape_news.py
python scrape_events.py
#mkdir daily_reviews/$date
#mkdir daily_reviews/$date/pdf

#python get_article_list.py daily_reviews/$date/rassegna.html
#python parse_html.py daily_reviews/$date/rassegna.html daily_reviews/$date/articles.csv

#python parse_html_polizia.py daily_reviews/$date/rassegna.html daily_reviews/$date/articles.csv
#python gui.py daily_reviews/$date/articles.csv
