from http.client import HTTPException
from fastapi import APIRouter, File, Security, UploadFile,Depends, status
from requests import Session
import models
from db_database import get_db
from auth import Auth
import shutil
from fastapi.security import  HTTPBearer,HTTPAuthorizationCredentials

def txt_len(filename):
    string = open(filename).read()
    count = 0
    for word in string.split():
        count+= len(word)
    return count

auth_handler = Auth()
security = HTTPBearer()

router = APIRouter(
    prefix='',
    tags=['Upload']
)

@router.post('/Word Count')
def upload(file: UploadFile = File(), db : Session = Depends(get_db),credentials: HTTPAuthorizationCredentials = Security(security)):
    with open(file.filename,'wb') as buffer:
            shutil.copyfileobj(file.file,buffer)

    token = credentials.credentials
    decoded = auth_handler.decode_token(token)
    user = db.query(models.User).filter(models.User.username == decoded).first()
    
    file_details = models.file_data(filename = file.filename,length = txt_len(file.filename),user_id = user.uuid)
    db.add(file_details)
    db.commit()
    db.refresh(file_details)
    
    return file_details
    
    




@router.get('/Get User stats')
def all(db : Session = Depends(get_db),credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials
        decoded = auth_handler.decode_token(token)
        user = db.query(models.User).filter(models.User.username == decoded).first()
        blogs = db.query(models.file_data).filter(models.file_data.user_id == user.uuid).all()
        total = 0
        for row in blogs:
            total+=row.length
        return {'user_id':user.uuid,'total_files_uploaded' :len(blogs),'total_words_counted':total}

            
    
'''@router.get('/{user_id}')
def show_User(id, db : Session = Depends(get_db),credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    decoded = auth_handler.decode_token(token)
    user = db.query(models.User).filter(models.User.username == decoded).first()
    files = db.query(models.User).filter(models.User.uuid == id).first()
    if not user:
        raise HTTPException(status_code=404,detail= f"User with the id {id} is not available")
    return user'''