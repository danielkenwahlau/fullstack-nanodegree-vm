#testing the database functions before placing them into webserver.py
import string
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

#print first result
firstResult = session.query(Restaurant).first()
print(firstResult.name)

allResults = session.query(Restaurant).all()

for entry in allResults:
    print(type(str(entry.name)))