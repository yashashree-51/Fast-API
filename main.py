from fastapi import FastAPI,Query,Depends
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,String,Integer,Boolean
from sqlalchemy.orm  import Session 
from database import Base,engine,SessionLocal
from fastapi import HTTPException


#model
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True) #This column will autoincrement why because primary key
    email = Column(String,unique=True,index=True)
    is_active = Column(Boolean,default=True)#this defines user is active or not

#schema
class UserSchema(BaseModel):
    id:int
    email:str
    is_active:bool

    class Config:
        orm_mode=True#if we have to return any objectthen we have to use orm mode



def get_db():#here we use dependency because we have many more api if we not use then we have to apply in every api then increase redundancy of code that's why
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)#this defines connecting to database

app = FastAPI()


@app.post("/users",response_model=UserSchema)
def index(user:UserSchema,db:Session=Depends(get_db)):
    #db work to put data into db
    u=User(email=user.email,is_active=user.is_active,id=user.id)
    db.add(u)
    db.commit()
    return u

@app.get("/users",response_model=List[UserSchema])
def index(db:Session=Depends(get_db)):
    return db.query(User).all()

@app.delete("/users/{user_id}", response_model=UserSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user