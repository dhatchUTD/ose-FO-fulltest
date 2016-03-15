from flask import Flask, request, redirect, url_for, render_template, \
		  session, flash, jsonify, g, send_from_directory, json
from flask.ext.triangle import Triangle
import pytz
import datetime
import os, sys, logging, logging.config

logging.config.fileConfig('rest_server_log.cfg')
MYLOG = logging.getLogger('rest.server')
MYLOG.info("Loading Simple REST SERVER")

from errors import ProcessError
from api_utils import MY_JSONEncoder
import api_test

app = Flask(__name__, template_folder='templates', static_folder='static')
app.json_encoder = MY_JSONEncoder

Triangle(app)

@app.route('/')
def index_page():
    return render_template('index_page.html', appjs = '', appName = '')

@app.route('/js/<path:path>')
def send_js(path):
    jspath = getattr( g, '_js_path', None)
    if jspath == None :
	jspath = g._js_path = os.path.join(os.path.dirname(__file__), 'js')
    return send_from_directory( jspath, path)

#test pages
#  uses_paperjs = 1 to load paperjs into the page


@app.route('/api/<libraryName>/<version>/<callName>', methods=['GET', 'POST'])
@app.route('/api/<libraryName>/<version>/<callName>/<param1>')
def api_call( libraryName, version, callName, param1 = None):
   timeString = datetime.datetime.now(pytz.utc).isoformat()
   if libraryName == "test":
        libraryFile = api_test
#   elif libraryName == "store":
#        libraryFile = api_store
   else:
        MYLOG.warning( "Unknown Library: "+libraryName)
        return jsonify ( error='Unknown API Library', timestamp=timeString)

   if hasattr( libraryFile, callName):
      if param1 == None and request.method == 'POST':
	  #MYLOG.debug( request.data)    
          param1 = json.loads( request.data)
      try:
        result = getattr( libraryFile, callName)( param1)
        response = jsonify ( results=result, timestamp=timeString)
        MYLOG.debug( "RESULTS: "+ response.get_data())
        return response
      except ProcessError as e:
        MYLOG.warning( e.msg)
        return jsonify ( error=e.msg, timestamp=timeString)
      except:
        MYLOG.error(sys.exc_info()[1],exc_info=True)
        return jsonify( error= "Unknown Error in Call", timestamp=timeString)
   else:
      MYLOG.warning("Unknown API CALL: "+callName)
      return jsonify ( error='Unknown API Call', timestamp=timeString)

   MYLOG.error("UNKNOWN ISSUE IN CALL")
   return jsonify( error= "Unknown Error", timestamp=timeString)


app.secret_key = 'Z3z748j:7lX R~X~H!jHN]LWX",?3r'

if __name__ == '__main__':
#    app.debug = True
    MYLOG.info( "Server ready for Requests ...")
    app.run(host='0.0.0.0', port=8086)

