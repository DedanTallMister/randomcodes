from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker (bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def DisplayRestaurants(restaurant_id):
	rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = rest.id)
	return render_template('menu.html', items = items, restaurant = rest)
	'''output = ''
	output += '<h1>%s</h1>' %rest.name
	for item in items:
		output += item.name
		output += '<br />'
		output += item.description
		output += '<br />'
		output += item.price
		output += '<br />'
		output += '<br />'
	return output'''
#Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash('New item created!!')
		return redirect(url_for('DisplayRestaurants', restaurant_id=restaurant_id))

	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)
# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		editedItem.name = request.form['edited']
		session.add(editedItem)
		session.commit()
		flash('An item has been edited')
		return redirect(url_for('DisplayRestaurants', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i = editedItem)
# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash('An item has been deleted')
		return redirect(url_for('DisplayRestaurants', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i = deletedItem)

    

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)


