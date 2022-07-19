from base64 import decode
from fastapi import APIRouter, File, Security, UploadFile,Depends, HTTPException, status
from requests import Session
import models
from db_database import get_db
from auth import Auth
import shutil
from fastapi.security import  HTTPBearer,HTTPAuthorizationCredentials
from word_count import txt_len,list_keywords,word_count,keywords_word_count


auth_handler = Auth()
security = HTTPBearer()

router = APIRouter(
    prefix='',
    tags=['Upload']
)

@router.post('/Word Count')
def upload(file: UploadFile = File(), db : Session = Depends(get_db),credentials: HTTPAuthorizationCredentials = Security(security)):
    if file.filename[-3:] != 'txt':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='File uploaded is not a text file \n Please upload text file')
    else:
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
                wordcount = word_count(file.filename)
                return wordcount
        else:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    
    


@router.post('/Word Count with keywords')
def upload(id, file: UploadFile = File(), db : Session = Depends(get_db),credentials: HTTPAuthorizationCredentials = Security(security)):
    if file.filename[-3:] != 'csv':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='File uploaded is not a .csv file \n Please upload .csv file')
    else:
        with open(file.filename,'wb') as buffer:
            shutil.copyfileobj(file.file,buffer)
        token = credentials.credentials
        decoded = auth_handler.decode_token(token)
        user = db.query(models.User).filter(models.User.username == decoded).first()
        if decoded == user.username:
            txt_file = db.query(models.file_data).filter(models.file_data.id == id).first()
            file_details = models.keywords(filename = file.filename, list_keywords = list_keywords(file.filename), user_id = user.uuid)
            all_files = []
            for i in db.query(models.keywords).filter(models.keywords.user_id== file_details.user_id).all():
                all_files.append(i.filename)
            if file_details.filename in all_files:
                return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='file already exists')
            else:
                db.add(file_details)
                db.commit()
                db.refresh(file_details)
                keyword_word_count = keywords_word_count(txt_file.filename,file.filename)
                return keyword_word_count
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