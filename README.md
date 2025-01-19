To run:
1. Create virtual environment and activate it if you wish.
2. Create tables in postgres
1. Run populate-stock.py 
2. Run search_wsb.py
3. Run display_top_stocks.py


About:
The first script populates your local db with stocks it gets from alpaca. 
The second script scrapes reddit using the PRAW Reddit API Wrapper to get any stock that is mentioned in a post's title(uses $ to determine what a stock is) and inserts it into a db
The third script cross references the two tables that had data inserted from the previous two scripts and prints out the top stocks mentioned (for that day)
