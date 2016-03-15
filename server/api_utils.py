from datetime import datetime
from pytz import timezone
from flask.json import JSONEncoder

class MY_JSONEncoder( JSONEncoder):

    def default(self, obj):
	if isinstance( obj, datetime):
	    #database stores times in US / Eastern tz
	    if obj.tzname() is None:
# strangely this doesn't work ... pytz has REASONS but offset comes out -4:56
#		return obj.replace( tzinfo=timezone('US/Eastern')).isoformat()
# whereas this one uses the modern and correct version
		return timezone('US/Eastern').localize( obj, is_dst=None)
	    return obj.isoformat()
	
	return JSONEncoder.default(self, obj)

