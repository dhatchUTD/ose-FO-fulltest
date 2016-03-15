import os, sys, json, logging, requests
from errors import ProcessError
import cx_Oracle

MYLOG = logging.getLogger( 'rest.server.api.test')

# oracle connect string user, password, database connect string
# change and uncomment
#db = cx_Oracle.connect('', '', '')

def calltest( params):
    MYLOG.debug( "Called calltest")
    MYLOG.debug( 'PARAMS: '+json.dumps(params))

    return "Hello World!"

def oracletest( params):
	MYLOG.debug( "Called oracletest")
	MYLOG.debug( 'PARAMS: '+json.dumps(params))

	response = {}
	
	cursor = db.cursor()
	# sql goes here
	cursor.execute('')

	response['call'] = cursor.fetchall()
	#MYLOG.debug( results)
	
	return response
	