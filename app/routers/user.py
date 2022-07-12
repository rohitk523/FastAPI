from lib2to3.pgen2 import token
from fastapi import APIRouter,Depends, HTTPException, Security,status
from requests import Session
import schemas,models
from db_database import get_db
from auth import Auth

router  = APIRouter(
    prefix='/user',
    tags=['User']
)

auth_handler = Auth()


@router.post('/')
def create_User(request: schemas.User, db : Session = Depends(get_db)):
    new_user = models.User(username= request.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = auth_handler.encode_token( new_user.username)
    decoded_token = auth_handler.decode_token(access_token)
    return {"access_token": access_token, "decode": decoded_token}





@router.get('/{user_id}',response_model=schemas.ShowUser)
def show_User(id, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404,detail= f"User with the id {id} is not available")
    return user

