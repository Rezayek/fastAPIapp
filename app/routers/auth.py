from fastapi import Response, status, HTTPException, Depends, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from .. import email


router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=schemas.Token)
async def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    
    if not user.is_verified:
        await email.send_email(schemas.EmailSchema(email = [user.email]), instance= user)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"account is not verified")
    
    #create Token
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


templates = Jinja2Templates(directory="templates")

@router.get('/verification', response_class= HTMLResponse)
async def email_verification(request: Request, token:str , db: Session = Depends(get_db)):
    user = oauth2.get_unverified_user(token = token)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Already Verified")
    
    db.query(models.User).filter(models.User.id == user.id).update({models.User.is_verified: True})
    
    return templates.TemplateResponse("verification.html", {"request": request, "username": user.username})
    
    
        
    
    