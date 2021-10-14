from typing import Optional, List, Union

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import RedirectResponse, JSONResponse

from sqlalchemy.orm import Session

from database import models, schemes, crud
from database.setup import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs/")


# region clients
@app.get("/clients/", response_model=Union[List[schemes.Client], schemes.Client])
def show_clients(client_id: Optional[int] = None, db: Session = Depends(get_db)):
    if client_id:
        return crud.get_client_by_id(db, client_id)
    else:
        return crud.get_clients(db)


@app.post("/clients/", response_model=schemes.ClientCreate)
def create_client(client: schemes.ClientCreate, db: Session = Depends(get_db)):
    test_client = crud.get_client_by_email(db, client.email)
    print(test_client)
    if test_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_client(db, client=client)
    return JSONResponse(status_code=200, content={"msg": "Successfully registered"})


@app.patch("/clients/", response_model=schemes.ClientUpdate)
def update_client(info: schemes.ClientUpdate, db: Session = Depends(get_db)):
    test_client1 = crud.get_client_by_id(db, info.id)
    test_client2 = crud.get_client_by_email(db, info.email)
    if not test_client1:
        raise HTTPException(status_code=400)
    if test_client2:
        if test_client1.email == test_client2.email:
            pass
        else:
            raise HTTPException(status_code=400, detail="Email already registered")
    crud.update_client(db, info)
    return JSONResponse(status_code=200, content={"msg": "Successfully updated"})


@app.delete("/clients/", response_model=schemes.ClientBase)
def delete_client(email: schemes.ClientBase, db: Session = Depends(get_db)):
    test_client = crud.get_client_by_email(db, email.email)
    if not test_client:
        raise HTTPException(status_code=400, detail="Client not found")
    crud.delete_client(db, email)
    return JSONResponse(status_code=200, content={"msg": "Successfully deleted"})


# Another variation
@app.get("/clients/{client_id}", response_model=schemes.Client)
def show_clients(client_id: int, db: Session = Depends(get_db)):
    return crud.get_client_by_id(db, client_id)

# endregion


# region orders
@app.post("/orders/", response_model=schemes.OrderCreate)
def add_order(order: schemes.OrderCreate, db: Session = Depends(get_db)):
    if crud.create_order(db, order):
        return JSONResponse(status_code=200, content={"msg": "Record added"})
    else:
        raise HTTPException(status_code=400, detail="Wrong client data")


@app.get("/orders/", response_model=Union[List[schemes.Order], schemes.Order])
def get_orders(client_id: Optional[int] = None,
               order_id: Optional[int] = None,
               db: Session = Depends(get_db)):
    print(client_id, order_id)
    if client_id and order_id:
        try:
            test_client = crud.get_client_by_id(db, client_id)
            # Will throw AttributeError if client won't be found
            # or IndexError if list is empty
            test_order = list(filter(lambda o: o.client_id == test_client.id and o.id == order_id,
                                     crud.get_orders(db)))[0]
            return test_order
        except (AttributeError, IndexError):
            raise HTTPException(status_code=400)
    else:
        return crud.get_orders(db)


@app.delete("/orders/", response_model=schemes.ClientBase)
def delete_order(data: schemes.OrderBase, db: Session = Depends(get_db)):
    test_order = crud.get_order(db, data.id)
    if not test_order:
        raise HTTPException(status_code=400, detail="Order not found")
    crud.delete_order(db, data)
    return JSONResponse(status_code=200, content={"msg": "Successfully deleted"})


@app.patch("/orders/", response_model=schemes.ClientBase)
def update_order(data: schemes.OrderUpdate, db: Session = Depends(get_db)):
    if not crud.get_order(db, data.id) or not crud.get_client_by_id(db, data.client_id):
        raise HTTPException(status_code=400)
    crud.update_order(db, data)
    return JSONResponse(status_code=200, content={"msg": "Record updated"})

# endregion


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
