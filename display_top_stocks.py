import config
import psycopg2
import psycopg2.extras

connection = psycopg2.connect(
    host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
show = cursor.execute("""
    SELECT COUNT(*) as num_mentions, stock_id, symbol
    FROM mention JOIN stock ON stock.id = mention.stock_id
    GROUP BY stock_id, symbol
    ORDER BY num_mentions DESC;
""")

mentions = cursor.fetchall()

for mention in mentions:
    print(mention)
