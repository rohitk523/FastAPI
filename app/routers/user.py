from fastapi import APIRouter,Depends, HTTPException,status
from requests import Session
import schemas,models
from db_database import get_db
from jwt_token import create_access_token
from fastapi.security import  OAuth2PasswordRequestForm


router  = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/')
def create_User(request: schemas.User, db : Session = Depends(get_db)):
    new_user = models.User(username= request.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Invalid Credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}





@router.get('/{user_id}',response_model=schemas.ShowUser)
def show_User(id, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTp,detail= f"User with the id {id} is not available")
    return user

