import uvicorn as uvicorn

from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Depends, UploadFile, File, Form, Response
from fastapi.encoders import jsonable_encoder

from pydantic import ValidationError

from sqlalchemy.orm import Session

from starlette import status
from starlette.responses import FileResponse

from db.schemas import Base
from db.crud import get_mp3
from db.database import engine, SessionLocal
from db.models import Name, UserData

from utils import user_add, check_user

from config import HOST, PORT


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "welcome to services wav to audio"}


@app.post("/users", status_code=201)
def add_user(user: Name, response: Response, db: Session = Depends(get_db)) -> dict:
    user_name: str = user.name
    data_user: dict = user_add(user_name, db)
    if not data_user:
        response.status_code = status.HTTP_200_OK
        return {"error_name": "user with name already is"}
    else:
        return data_user


def checker(data: str = Form(...)):
    try:
        model = UserData.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return model


@app.post("/users/wav", status_code=200)
def add_audio(response: Response, record: UserData = Depends(checker),
              audio_file: UploadFile = File(...),
              db: Session = Depends(get_db)) -> str:
    file_check = check_user(db, {"user_id": record.user_id, "token": record.access_token}, audio_file)
    if not file_check:
        response.status_code = status.HTTP_200_OK
        return "such a file already is"
    else:
        return file_check


@app.get("/record")
def get_audio(id: str, db: Session = Depends(get_db)):
    path: str = get_mp3(db, id)
    return FileResponse(path=path, filename=path, media_type="application/octet-stream")


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
