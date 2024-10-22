from fastapi import *
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from fastapi import status
import schemas
import utils

router = APIRouter()

@router.post("/post", status_code=status.HTTP_201_CREATED)
def createuser(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/post/{id}',response_model = schemas.UserOut)

def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} does not exist.")
    return user
    