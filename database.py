import pandas as pd
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()
engine = db.create_engine("sqlite:///red-bus-data.db")


class buses(Base):
    __tablename__ = 'red-bus-data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_name = db.Column(db.String(100))
    route_link = db.Column(db.String(300))
    busname = db.Column(db.String(100))
    bustype = db.Column(db.String(100))
    departing_time = db.Column(db.Time)
    duration = db.Column(db.String(100))
    reaching_time = db.Column(db.Time)
    star_rating = db.Column(db.Float)
    price = db.Column(db.DECIMAL)
    seats_available = db.Column(db.Integer)


Session = sessionmaker(bind=engine)
session = Session()

# Base.metadata.create_all(engine)

df = pd.read_csv('all_buses_data3.csv')

total_rows = df.shape[0]
c = 1
for index, row in df.iterrows():
    try:
        bus = buses(route_name=row[1], route_link=row[2], busname=row[3], bustype=row[4], departing_time=datetime.strptime(row[5], '%H:%M').time(),duration=row[6], reaching_time=datetime.strptime(row[7], '%H:%M').time(), price=row[9], seats_available=row[10])
        if row[8] == "New":
            bus.star_rating = 1000
        else:
            bus.star_rating = row[8]

        session.add(bus)
        session.commit()
        print(f"{c}/{total_rows} - insertion - done")
        c += 1
    except Exception as e:
        session.rollback()
        print(str(e))
        print(index, row)

