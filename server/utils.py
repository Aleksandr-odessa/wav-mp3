from uuid import uuid4
import jwt

from config import FILE_LOCATION, ALGORITHM, HOST, PORT
from db.crud import add_user_to_db, add_file, get_id, get_user
from pydub import AudioSegment
from fastapi import UploadFile, File
import pathlib


def user_add(user_name: str, db) -> dict | None:
    user = get_user(user_name, db)
    if not user:
        user_id: str = str(uuid4())
        token: str = generate_token(user_name, user_id)
        data_user: dict = {"user_name": user_name, "user_id": user_id, "token": token}
        add_user_to_db(data_user, db)
        return {"user_id": user_id, "token": token}


def generate_token(user_name: str, user_id: str) -> str:
    payload = {"some": user_name}
    return jwt.encode(payload, user_id, algorithm=ALGORITHM)


def check_user(db, request_user: dict, audio_file: UploadFile = File(...)) -> str | None:
    id_user: str = request_user['user_id']
    token_user: dict | None = get_id(db, id_user)
    if not token_user:
        return 'User ID is invalid'
    elif request_user['token'] != token_user['token']:
        return 'Token is invalid'
    else:
        record_id = convert_to_mp3(audio_file, db)
        return f"http://{HOST}:{PORT}/record?id={record_id}&user={id_user}" if record_id else None


def convert_to_mp3(audio_file, db) -> str | None:
    record_id: str = str(uuid4())
    file_path: str = f'{FILE_LOCATION}/{audio_file.filename}'
    if not pathlib.Path(file_path).exists():
        wav_audio = AudioSegment.from_wav(audio_file.file)
        wav_audio.export(file_path, format="wav")
        file_path_mp3: str = f'{file_path[:-4]}.mp3'
        wav_audio.export(file_path_mp3, format="mp3")
        data_audio: dict = {'file_id': record_id, 'file_path': file_path_mp3}
        add_file(db, data_audio)
        return record_id
