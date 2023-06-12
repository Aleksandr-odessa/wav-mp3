from uuid import uuid4

import jwt
from sqlalchemy.orm import Session

from config import ALGORITHM
from db.schemas import Audio, Users


def add_user_to_db(user_name: str, db: Session) -> dict:
    user_id: str = str(uuid4())
    token: str = jwt.encode({"some": user_name}, user_id, algorithm=ALGORITHM)
    data_user = Users(id_user=user_id, name=user_name, token=token)
    db.add(data_user)
    db.commit()
    db.refresh(data_user)
    return {"user_id": user_id, "token": token}


def is_user_exist(user: str, db: Session) -> bool:
    return True if db.query(Users).filter(Users.name == user).first() else False


def get_token(db: Session, id_user: str) -> str | None:
    token: Users | None = db.query(Users).filter(Users.id_user == id_user).first()
    if token:
        return token.token


def add_file(db: Session, audio: dict) -> None:
    files = Audio(file_id=audio['file_id'], audio_file=audio['file_path'])
    db.add(files)
    db.commit()


def get_mp3(db: Session, id_file: str) -> str:
    path_file: Audio = db.get(Audio, id_file)
    return path_file.audio_file
