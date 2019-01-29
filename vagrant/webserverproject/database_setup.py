import sys
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()



#Start of end of file setup

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
#End of end of file setup
