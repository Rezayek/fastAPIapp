
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from .. import email

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
async def create_suser(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #Hash the password
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    await email.send_email(schemas.EmailSchema(email = [user.email]), instance= new_user)
    
    return new_user

@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user id: {id} not found")
    
    return user
