#!/usr/bin/env python3

import psycopg2

DATABASE = "news"

question_1="Question 1. What are the most popular three articles of all time?"
question_2="Question 2. Who are the most popular article authors of all time?"
question_3="Question 3. On which days did more than 1% of requests lead to errors?"

sql_query_1="""
	SELECT articles.title, count(*) as views from articles, log
	where CONCAT('/article/', articles.slug) LIKE log.path 
	group by articles.title 
	order by views desc
	limit 3;
"""
sql_query_2=""
sql_query_3="""
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
	WHERE views_all.day = views_error.day and views_error.count::real / views_all.count::real *100>1;
"""



def queryDb(query):
	"""Connects to database and executes the query.
	Argument:	
	"""
	db= psycopg2.connect(database=DATABASE)
	c=db.cursor()
	c.execute(query)
	result = c.fetchall()
	db.close()
	return result

def hello():
	print "#########################################"
	print "Hi. This the log analysis project for the full stack webdeveloper nanodegree by Udacity.\n"

def ask3Questions():	
	"""Queries the database with 3 (questions) SQL queries."""
	print question_1
	response_1 = queryDb(sql_query_1)
	counter = 1
	for element in response_1:		
		print (str(counter)+'. '+str(element[0])+', views: '+str(element[1]))
		counter += 1
	print 
	print
	
	print question_3	
	response_3 = queryDb(sql_query_3)
	for element in response_3:
		print("DAYS : CORRECT VIEWS : ERROR VIEWS: ERROR %")
		print (str(element[0])+' : '+ str(element[1])+' : '+ str(element[2])+' : '+ str(element[3]))
	print
	
if __name__ == "__main__":
	hello()
	ask3Questions()
	#print queryDb(sql_query_1)
	
	
	
	print question_3
