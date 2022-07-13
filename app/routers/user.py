from fastapi import APIRouter,Depends, HTTPException
from requests import Session
import schemas,models
from db_database import get_db
from auth import Auth
import uuid

router  = APIRouter(
    prefix='/user',
    tags=['User']
)

auth_handler = Auth()


@router.post('/')
def create_User(request: schemas.User, db : Session = Depends(get_db)):
    new_uuid = str(uuid.uuid4())
    new_user = models.User(username= request.username,uuid = new_uuid)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = auth_handler.encode_token( new_user.username)
    return {"access_token": access_token, "uuid": new_uuid}







