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
user_id_ = 2
auth_handler = Auth()
security = HTTPBearer()

router = APIRouter(
    prefix='/Word Count',
    tags=['Upload']
)

@router.post('/')
def upload(file: UploadFile = File(), db : Session = Depends(get_db),credentials: HTTPAuthorizationCredentials = Security(security)):
    with open(file.filename,'wb') as buffer:
            shutil.copyfileobj(file.file,buffer)
    file_details = models.file_data(filename = file.filename,length = txt_len(file.filename),user_id = user_id_)
    db.add(file_details)
    db.commit()
    db.refresh(file_details)
    user = db.query(models.User).filter(models.User.id == user_id_).first()
    token = credentials.credentials
    decoded = auth_handler.decode_token(token)
    try:
        if decoded == user.username:
            
            return file_details
    except:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    
    




@router.get('/Get overall stats/')
def all(db : Session = Depends(get_db),credentials: HTTPAuthorizationCredentials = Security(security)):
        user = db.query(models.User).filter(models.User.id == user_id_).first()
        token = credentials.credentials
        decoded = auth_handler.decode_token(token)
        try:
            if  decoded == user.username:
                blogs = db.query(models.file_data).filter(models.file_data.user_id == user_id_).all()
                total = 0
                for row in blogs:
                    total+=row.length

                return {'user_id':user_id_,'total_files_uploaded' :len(blogs),'total_words_counted':total}
        except:
            raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

            
    
