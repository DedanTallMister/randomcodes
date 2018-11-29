from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith('/edit'):
				restNumber = self.path.split("/") [2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restNumber).one()
				if myRestaurantQuery !=[]:
					self.send_response(200)
        		        	self.send_header('Content-type', 'text/html')
        		        	self.end_headers()
        		        	output = '<html><body>'
					output += '<h1>Make a new restaurant</h1>'
					output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" %restNumber
					output += "<input name='Edited' type = 'text' placholder = 'Edited'>"
					output += "<input type = 'submit' value = 'Rename'>"
					output += "</body></html>"
					self.wfile.write(output)
			if self.path.endswith('/del'):
				restNumber = self.path.split('/') [2]
				RestaurantQuery = session.query(Restaurant).filter_by(id = restNumber).one()
				if RestaurantQuery != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = '<html><body>'
					output += '<h1>Are you sure you want to delete the following Restaurant: %s?</h1>'%RestaurantQuery.name
					output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/del'>" %restNumber
					output += "<input type = 'submit' value = 'Elimina'>"
					output += "</body></html>"
					self.wfile.write(output)

			if self.path.endswith('/restaurants/new'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = '<html><body>'
				output += '<h1>Make a new restaurant</h1>'
				output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<input name='newRestaurantName' type = 'text' placholder = 'newRestaurantName'>"
				output += "<input type = 'submit' value = 'Create'>"
				output += "</body></html>"
				self.wfile.write(output)
				return
			if self.path.endswith('/restaurants'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = '<html><body>'
				rests = session.query(Restaurant).all()
				for rest in rests:
					output += '<h1>%s</h1>' %rest.name
					output += "<a href = '/restaurants/%s/del'> DELETE </a> <br />" %rest.id
					output += "<a href = 'restaurants/%s/edit'> EDIT </a> <br /><br />" %rest.id
				output += "<a href = '/restaurants/new'><button type = 'button'>Inserisci nuovo</button></a>"
				output += "</body></html>"
				self.wfile.write(output)
				return
		except IOError:
			self.send_error(404, 'File not found %s' %self.path)
	def do_POST(self):
		try:
			if self.path.endswith('/edit'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('Edited')
				restNumber = self.path.split("/") [2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restNumber).one()
				if myRestaurantQuery !=[]:
					myRestaurantQuery.name = messagecontent[0]
					session.add(myRestaurantQuery)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers

			if self.path.endswith('/del'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
				restNumber = self.path.split('/')[2]
				RestaurantQuery = session.query(Restaurant).filter_by(id = restNumber)
				if RestaurantQuery != []:
					session.delete(RestaurantQuery)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers
				
			if self.path.endswith('/restaurants/new'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
				newRestaurant = Restaurant(name = messagecontent[0])
				session.add(newRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print 'Webserver running on port %s' %port
		server.serve_forever()

	except KeyboardInterrupt:
		print ' Entered, stopping server'
		server.socket.close()
if __name__ == '__main__':
	main()