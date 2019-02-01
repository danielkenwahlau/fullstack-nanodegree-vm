#creates Database and adds the restaurant and one menu item

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


#lets the program know which database we want to communicate with
engine = create_engine('sqlite:///restaurantmenu.db')

#binds engine to base class
Base.metadata.bind = engine

#make session which est a conn between code execution and engine we just created
DBSession = sessionmaker(bind = engine)

session = DBSession()

#The sessions works by creating and object then adding it to the staging area. Then
#When you have everything in the staging area you commit to add to the database.
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

#goes into the table and finds all entries in that table and returns it in a list
session.query(Restaurant).all()


#adding a menu item
cheesepizza = MenuItem(name = "Cheese Pizza",
    description = "Made with all natural ingredients and ",
    course = "Entree",
    price = "$8.99",
    restaurant = myFirstRestaurant)

session.add(cheesepizza)
session.commit()
session.query(MenuItem).all()