from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
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