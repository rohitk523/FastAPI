from base64 import decode
from fastapi import APIRouter, File, Security, UploadFile,Depends, HTTPException, status
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
    if decoded == user.username:
        file_details = models.file_data(filename = file.filename,length = txt_len(file.filename),user_id = user.uuid)
        all_files = []
        for i in db.query(models.file_data).filter(models.file_data.user_id== file_details.user_id).all():
            all_files.append(i.filename)
        if file_details.filename in all_files:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='file already exists')
        else:
            db.add(file_details)
            db.commit()
            db.refresh(file_details)
            return file_details
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    
    
    




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