import uvicorn as uvicorn
from fastapi import Depends, FastAPI, File, Form, Response, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import FileResponse

from config import HOST, PORT
from db.crud import add_user_to_db, get_mp3, is_user_exist
from db.database import SessionLocal, engine
from db.models import Name, UserData
from db.schemas import Base
from config_log import logger
from utils import convert_to_mp3

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "welcome to services wav to audio"}


@app.post("/users", status_code=201)
def add_user(user: Name, response: Response, db: Session = Depends(get_db)) -> dict:
    user_name: str = user.name
    is_user: bool = is_user_exist(user_name, db)
    if is_user:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.error('Username already in use')
        return {"message_error": "Username already in use"}
    else:
        return add_user_to_db(user_name, db)


def checker_form_user_data(data: str = Form(...)) -> UserData:
    try:
        model = UserData.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return model


@app.post("/users/wav", status_code=200)
def convert_audio(response: Response, record: UserData = Depends(checker_form_user_data),
              audio_file: UploadFile = File(...),
              db: Session = Depends(get_db)) -> str:
    data_user: dict = {"user_id": record.user_id, "token": record.access_token}
    http_path_file_mp3: dict = convert_to_mp3(data_user, db, audio_file)
    match list(http_path_file_mp3.keys()):
        case ['error_data']:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return http_path_file_mp3.get("error_data")
        case ['error_file']:
            response.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            return http_path_file_mp3.get("error_file")
        case ['message']:
            return http_path_file_mp3.get("message")


@app.get("/record")
def download_audio(id: str, db: Session = Depends(get_db)) -> FileResponse:
    dowload_path: str = get_mp3(db, id)
    return FileResponse(path=dowload_path, filename=dowload_path[6:], media_type="application/octet-stream")


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
