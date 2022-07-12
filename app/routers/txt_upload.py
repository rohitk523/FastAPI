from fastapi import APIRouter, File, Form, UploadFile,Depends
from requests import Session
from oauth2 import get_current_user
import schemas,models
from db_database import get_db
import shutil

def txt_len(filename):
    string = open(filename).read()
    count = 0
    for word in string.split():
        count+= len(word)
    return count

router = APIRouter(
    prefix='/Word Count',
    tags=['Upload']
)

@router.post('/')
def upload(file: UploadFile = File(), db : Session = Depends(get_db)):
    with open(file.filename,'wb') as buffer:
        shutil.copyfileobj(file.file,buffer)
    file_details = models.file_data(filename = file.filename,length = txt_len(file.filename),user_id = 2)
    db.add(file_details)
    db.commit()
    db.refresh(file_details)
    return file_details

@router.get('/All files')
def all( db : Session = Depends(get_db)):
    blogs = db.query(models.file_data).all()
    return blogs 

@router.get('/Get User stats')
def all( db : Session = Depends(get_db)):
    blogs = db.query(models.file_data.length).all()
    user_id = db.query(models.file_data.user_id)
    total = 0
    for row in blogs:
        total+=row.length

    return {'total_files_uploaded” ':len(blogs),'total_words_counted':total}

