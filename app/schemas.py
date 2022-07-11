from re import L
from fastapi import UploadFile
from typing import List
from unicodedata import name
from pydantic import BaseModel
from typing import Union
import schemas


class User(BaseModel):
    username: str

class filedata(BaseModel):
    filename :str
    length : int
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    username: str
    textFiles: List[filedata] = []
    class Config():
        orm_mode = True


class Showfile(BaseModel):
    filename: str
    length : int
    creator : ShowUser
    class Config():
        orm_mode = True





class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class Login(BaseModel):
    username: str
    password: str

