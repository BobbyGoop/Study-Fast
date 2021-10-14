from sqlalchemy.orm import Session

from . import models, schemes


# region CLIENTS
def get_client_by_id(db: Session, user_id: int):
    return db.query(models.Client).filter(models.Client.id == user_id).first()


def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: schemes.ClientCreate) -> None:
    print(client)
    db_user = models.Client(client.email, client.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print("returning ...")


def update_client(db: Session, client: schemes.ClientUpdate) -> None:
    test_client = db.query(models.Client).get(client.id)
    for attr in list(client.dict().keys()):
        setattr(test_client, attr, client.dict()[attr])
        db.flush()
    db.commit()


def delete_client(db: Session, client: schemes.ClientBase) -> None:
    db.delete(db.query(models.Client).filter(models.Client.email == client.email).first())
    db.commit()

# endregion


# region ORDERS
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    print("crud")
    return db.query(models.Order).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int):
    return db.query(models.Order).get(order_id)


def delete_order(db: Session, order: schemes.OrderBase):
    db.delete(db.query(models.Order).filter(models.Order.id == order.id).first())
    db.commit()


def create_order(db: Session, order: schemes.OrderCreate):
    test_client = db.query(models.Client).get(order.client_id)
    if test_client is None:
        return False
    new_order = models.Order(test_client.id,  test_client.name, order.total)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return True


def update_order(db: Session, data: schemes.OrderUpdate) -> None:
    test_order = db.query(models.Order).get(data.id)
    full_data = {k: v for k, v in data.dict().items()}
    full_data['client_name'] = db.query(models.Client).get(full_data['client_id']).name
    for attr, val in full_data.items():
        setattr(test_order, attr, val)
        db.flush()
    db.commit()
# endregion
