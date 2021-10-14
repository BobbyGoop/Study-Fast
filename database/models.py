from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.setup import Base


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    surname = Column(String(250))
    password = Column(String(100))
    email = Column(String(250), unique=True)
    orders = relationship("Order", back_populates = "client")

    # TODO: finish up with password encryption
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "{} {} {}".format(self.id, self.name, self.surname)

    def serialize(self):
        return {"data": self.id, "name": self.name, "surname": self.surname, "email": self.email}


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)

    client_id = Column(Integer, ForeignKey('clients.id'))
    client_name = Column(String, nullable=False)
    client = relationship("Client", back_populates = "orders")

    created_at = Column(DateTime, nullable=False)
    total = Column(Integer, nullable=False)

    def __init__(self, client_id, client_name, total):
        self.client_id = client_id
        self.client_name = client_name
        self.total = total
        self.created_at = datetime.now()

    def __repr__(self):
        return "{} {} {}".format(self.id, self.client_name, self.total)

    def serialize(self):
        return {"data": self.id, "client_name": self.client_name,
                "client_id": self.client_id, "created_at": str(self.created_at),
                "total": self.total}

