from fastapi import *
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from routers import user,auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"Message": "Hello"}

app.include_router(user.router)
app.include_router(auth.router)
