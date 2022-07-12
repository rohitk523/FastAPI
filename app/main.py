from multiprocessing import synchronize
from fastapi import Depends, FastAPI
from routers import user,txt_upload
import models,db_database

app = FastAPI()

models.Base.metadata.create_all(bind=db_database.engine)

app.include_router(user.router)
app.include_router(txt_upload.router)


#current_user: schemas.User = Depends(get_current_user)



