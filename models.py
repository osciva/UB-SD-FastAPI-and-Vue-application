import enum

from sqlalchemy import Boolean, MetaData, Column, ForeignKey, Integer, String, Date, DateTime, Float, Enum, UniqueConstraint, Table
from sqlalchemy.orm import relationship

from database import Base


class Team(Base):
    __tablename__ = 'teams' #This is table name

    id = Column(Integer, primary_key=True)
    name: str = Column(String(30),unique=True, nullable=False, index=True)
    country = Column(String(30),nullable=False)
    description = Column(String(100))

teams_in_competitions = Table("teams_in_competitions",Base.metadata,
                                 Column("id", Integer, primary_key=True),
                                 Column("team_id", Integer, ForeignKey("teams.id")),
                                 Column("competition_id",Integer, ForeignKey("competitions.id")))




class Category(str, enum.Enum):
    Senior = "Senior"
    Junior = "Junior"

class Sports(str, enum.Enum):
    Volleyball = "Volleyball"
    Football = "Football"
    Futsal = "Futsal"
    Basketball = "Basketball"
    Tennis = "Tennis"

# categories_list = ("Senior","Junior")
# sports_list = ("Volleyball","Football")
categories_list = (Category)
sports_list = (Sports)

class Competition(Base):

    __tablename__ = 'competitions'  # This is table name
    __table_args__ = (UniqueConstraint('name', 'category', 'sport'),)

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    category = Column(Enum(*categories_list),nullable=False)
    sport = Column(Enum(*sports_list),nullable=False)
    teams = relationship("Team",secondary=teams_in_competitions,backref="competitions")
    match = relationship("Match", backref="competitions")

class Match(Base):
    __tablename__ = 'matches' #This is table name
    __table_args__ = (UniqueConstraint('local_id', 'visitor_id', 'competition_id', 'date'),) #'local_id', 'visitor_id' #Esto indica que no puede repetirse

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    total_available_tickets = Column(Integer)
    #local = Column(String(30), nullable=False)
    #visitor = Column(String(30), nullable=False)
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    competition = relationship("Competition", backref="matches")

    local_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    visitor_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    local = relationship("Team", foreign_keys=local_id)
    visitor = relationship("Team", foreign_keys=visitor_id)

class Account(Base):
    __tablename__ = 'accounts'

    username = Column(String(30), primary_key=True, unique=True, nullable=False)
    password = Column(String(), nullable=False)
    # 0 not admin/ 1 is admin
    is_admin = Column(Integer, nullable=False)
    available_money = Column(Float, nullable=False)
    orders = relationship('Order', backref='orders', lazy=True)

    def __init__(self, username, available_money=200, is_admin=0):
        self.username = username
        self.available_money = available_money
        self.is_admin = is_admin
        self.password = "test"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), ForeignKey('accounts.username'), nullable=False)
    match_id = Column(Integer, nullable=False)
    tickets_bought = Column(Integer, nullable=False)

    def __init__(self, match_id, tickets_bought):
        self.match_id = match_id
        self.tickets_bought = tickets_bought


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)