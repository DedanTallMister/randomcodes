from flask import Flask
app = Flask(__name__)

DBSession = sessionmaker (bind = engine)
sesion = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
	rest = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = rest.id)
	output = ''
	output += '<h1>%s</h1>' %rest.name
	for item in items:
		output += item.name
		output += '<br />'
	return output

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)