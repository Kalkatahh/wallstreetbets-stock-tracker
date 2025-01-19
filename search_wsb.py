import praw
import config
import datetime 
import psycopg2
import psycopg2.extras
from requests import Session

connection = psycopg2.connect(
    host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("""
    SELECT * FROM stock
""")
rows = cursor.fetchall()


stocks = {}
for row in rows:
    stocks['$' + row['symbol']] = row['id']

session = Session()
reddit = praw.Reddit( 
    client_id= config.REDDIT_CLIENT_ID,
    client_secret= config.REDDIT_CLIENT_SECRET,
    user_agent= config.REDDIT_USER_AGENT,
    username= config.REDDIT_USERNAME,
    password= config.REDDIT_PASSWORD,
    requestor_kwargs={"session": session},
)



subreddit = reddit.subreddit('wallstreetbets')

submissions = subreddit.new(limit=None)  # Fetch new posts

start_time = int(datetime.datetime(2021, 2, 14).timestamp())

for submission in submissions:
    words = submission.title.split()
    cashtags = list(set(filter(lambda word: word.startswith('$') and (len(word) > 1 and not word[1].isdigit()), words)))
    for cashtag in cashtags:
        submitted_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()
        if len(cashtags) > 0:
            try:

                cursor.execute("""
                    INSERT INTO mention (dt, stock_id, message, source, url)
                    VALUES (%s, %s, %s, 'wallstreetbets', %s)
                """, (submitted_time, stocks[cashtag], submission.title, submission.url))


                connection.commit()
            except Exception as e:
                print(f"Error inserting row: {e}")
                connection.rollback()


print("All submissions processed successfully!")


try:
    cursor.execute("SELECT * FROM mention")
    mentions = cursor.fetchall()
    for mention in mentions:
        print(mention)
except Exception as e:
    print(f"Error fetching data: {e}")
