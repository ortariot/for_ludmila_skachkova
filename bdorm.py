import sqlalchemy
from sqlalchemy import sesessionmaker
from models import create_tables, User


DSN = "postgresql://postgres:12345678@localhost:5432/LudmilaSka"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()





session.close()
