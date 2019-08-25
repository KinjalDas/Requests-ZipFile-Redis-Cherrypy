import cherrypy, redis, os, json

class HelloWorld(object):
	@cherrypy.expose
	def index(self):
		return open('index.html')

@cherrypy.expose
class DBValuesGenerator(object):
	def __init__(self,redisclient):
		self.redisclient = redisclient
		self.records = int(self.redisclient.get("records"))
	@cherrypy.tools.accept(media='text/plain')
	def GET(self,records=10):
		records = int(records)
		list_records = []
		limit = self.records
		if records>limit:
			records = limit
		for i in range(records):
			record_dict = {}
			record_dict['code'] = int(self.redisclient.hget(i,'code'))
			record_dict['name'] = self.redisclient.hget(i,'name').decode()
			record_dict['open'] = float(self.redisclient.hget(i,'open'))
			record_dict['high'] = float(self.redisclient.hget(i,'high'))
			record_dict['low'] = float(self.redisclient.hget(i,'low'))
			record_dict['close'] = float(self.redisclient.hget(i,'close'))
			list_records.append(record_dict)
		return json.dumps(list_records)

	def POST(self,search_string):
		code_list = []
		name_list = []
		open_list = []
		high_list = []
		low_list = []
		close_list = []
		record_dict = {}
		for i in range(self.records):
			if self.redisclient.hget(i,'name').decode().find(search_string) != -1:
				code_list.append(int(self.redisclient.hget(i,'code')))
				name_list.append(self.redisclient.hget(i,'name').decode())
				open_list.append(float(self.redisclient.hget(i,'open')))
				high_list.append(float(self.redisclient.hget(i,'high')))
				low_list.append(float(self.redisclient.hget(i,'low')))
				close_list.append(float(self.redisclient.hget(i,'close')))
		record_dict['codes'] = code_list 
		record_dict['names'] = name_list
		record_dict['opens'] = open_list
		record_dict['highs'] = high_list
		record_dict['lows'] = low_list
		record_dict['closes'] = close_list
		return json.dumps(record_dict)

if __name__ == '__main__':
	conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
	redisClient = redis.StrictRedis(host='localhost',port=6379,db=0)
	webapp = HelloWorld()
	webapp.generator = DBValuesGenerator(redisClient)
	cherrypy.quickstart(webapp, '/', conf)