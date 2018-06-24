#!/usr/bin/env python3

import psycopg2

DATABASE = "news"

question_1 = "Question 1. What are the most popular three articles of all time?"
sql_query_1 = """
    SELECT articles.title, count(*) as views from articles, log
    where CONCAT('/article/', articles.slug) LIKE log.path 
    group by articles.title 
    order by views desc
    limit 3;
    """

question_2 = "Question 2. Who are the most popular article authors of all time?"
sql_query_2 = """
    SELECT authors.name, count(articles.author) as views FROM log, authors, articles
    WHERE log.status = '200 OK'
    and articles.slug = substr(log.path, 10)
    and articles.author = authors.id
    group by authors.name
    order by views desc;
    """

question_3 = "Question 3. On which days did more than 1% of requests lead to errors?"
sql_query_3 = """
    WITH
    views_all AS (
    SELECT date(time) AS day, count(*) FROM log
    GROUP BY day
    ORDER BY day
    ),
    views_error AS (
    SELECT date(time) AS day, count(*) FROM log
    WHERE status = '404 NOT FOUND'
    GROUP BY day
    ORDER BY day
    )
    SELECT views_all.day, views_all.count as ok, views_error.count as errors, 
    views_error.count::real / views_all.count::real *100  AS errors_percent
    FROM views_all, views_error
    WHERE views_all.day = views_error.day 
    and views_error.count::real / views_all.count::real * 100 > 1;
    """

def queryDb(query):
    """Connects to database and executes the query.
    
    Args:
        query: SQL statement that will be executed.
    """    
    try:
        db = psycopg2.connect(database=DATABASE)
        c = db.cursor()
        c.execute(query)
        result = c.fetchall()
        db.close()
        return result
    except:
        print('Error! Could not connect or execute query!')        

def hello():
    """Short intro to the python program."""
    
    print"This is the log analysis project for the full stack webdeveloper nanodegree."
    print"This short program queries a database with 3 SQL statements."        

def query_Questions():
    """Queries the database with 3 (questions) SQL queries."""
        
    print question_1
    response_1 = queryDb(sql_query_1)
    counter = 1
    for element in response_1:        
        print (str(counter) + '. ' + str(element[0]) + ', views: ' + str(element[1]))
        counter += 1
    print 
    print
    
    print question_2
    response_2 = queryDb(sql_query_2)
    print("AUTHOR NAME: VIEWS")
    for element in response_2:
        print(str(element[0]) +' : '+ str(element[1]))
    print
    print        
    
    print question_3    
    response_3 = queryDb(sql_query_3)
    print("DAYS : CORRECT VIEWS : ERROR VIEWS: ERROR %")
    for element in response_3:        
        print (str(element[0]) + ' : ' + str(element[1]) +
		' : ' + str(element[2]) + ' : ' + str(element[3]))
    print

if __name__ == "__main__":
    hello()
    query_Questions()
