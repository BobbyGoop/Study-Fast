from datetime import date
from pydantic import BaseModel
from typing import List


class OrderBase(BaseModel):
	id: int


class OrderCreate(BaseModel):
	client_id: int
	total: int


class OrderUpdate(OrderBase, OrderCreate):
	pass


class Order(OrderCreate, OrderBase):
	client_name: str
	created_at: date

	class Config:
		orm_mode = True


class ClientBase(BaseModel):
	email: str


class ClientCreate(ClientBase):
	password: str


class ClientUpdate(ClientBase):
	id: int
	name: str
	surname: str


class Client(ClientBase):
	id: int
	name: str
	surname: str
	orders: List[Order] = []

	class Config:
		orm_mode = True
