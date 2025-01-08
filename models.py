from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Scraped(Base):
    __tablename__ = "scraped"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    coupon = Column(String)
    category = Column(String)


class Claimed(Base):
    __tablename__ = "claimed"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    category = Column(String)


# Create an SQLite database
engine = create_engine("sqlite:///Example.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
