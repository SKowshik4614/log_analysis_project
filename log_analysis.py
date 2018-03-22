import psycopg2
def connect(dbname = "news"):
  """Connect to the PostgreSQL database and returns a database connection."""
  try:
    db = psycopg2.connect("dbname={}".format(dbname))
    c = db.cursor()
    return db, c
  except:
      print("Error in connecting to database")

def popular_article():
  db, c = connect()
  q1 = "create or replace view popular_articles as\
    select title, count(title) as views from articles,log\
    where log.path = concat('/article/',articles.slug)\
    group by title order by views desc limit 3"
  c.execute(q1)
  print("Most Popular 3 Articles:")
  query = "select * from popular_articles"
  c.execute(query)
  for (title, views) in c.fetchall():
        print("{} ==> {} views".format(title, views))
  db.commit()
  db.close()

def popular_authors():
  db, c = connect()
  q2 = "create or replace view popular_authors as select authors.name,\
        count(articles.author) as views from articles, log, authors where\
        log.path = concat('/article/',articles.slug) and\
        articles.author = authors.id group by authors.name order by views desc"
  c.execute(q2)
  print("Most Popular Article Authors of All Time:")
  query = "select * from popular_articles"
  c.execute(query)
  for (name, view) in c.fetchall():
        print("{} ==> {} views".format(name, view))
  db.commit()
  db.close()

def log_status():
  db, c = connect()
  q3 = "create or replace view log_status as select Date,Total,Error,\
        (Error::float*100)/Total::float as Percent from\
        (select time::timestamp::date as Date, count(status) as Total,\
        sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error\
        from log group by time::timestamp::date) as out\
        where (Error::float*100)/Total::float > 1.0 order by Percent desc"
  c.execute(q3)
  print("More than 1% of Requests Errors:")
  query = "select * from log_status"
  c.execute(query)
  out = c.fetchall()
  for i in range(0, len(out), 1):
        print str(out[i][0])+ " ==> "+str(round(out[i][3], 2))+"% errors"
  db.commit()
  db.close()

if __name__ == '__main__':
  popular_article()
  popular_authors()
  log_status()
