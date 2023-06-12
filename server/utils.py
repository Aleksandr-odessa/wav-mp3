import pathlib
import time
from uuid import uuid4

from fastapi import File, UploadFile
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from sqlalchemy.orm import Session

from config import FILE_LOCATION, HOST, PORT
from db.crud import add_file, get_token
from config_log import logger


def convert_to_mp3(data_user: dict, db: Session, audio_file: UploadFile = File(...)) -> dict | None:
    error_received_data: str = error_id_user_or_token_user(data_user, db)
    if error_received_data:
        return {"error_data": error_received_data}
    record_id: str = str(uuid4())
    file_path: str = f'{FILE_LOCATION}/{audio_file.filename}'
    try:
        wav_audio = AudioSegment.from_wav(audio_file.file)
    except CouldntDecodeError:
        logger.error("Couldn't read wav audio from data")
        return {"error_file":"Couldn't read wav audio from data"}
    wav_audio.export(file_path, format="wav")
    if pathlib.Path(file_path).exists():
        sec = str(time.time()).split('.')[0]
        file_path_mp3: str = f'{file_path[:-4]}{sec}.mp3'
    else:
        file_path_mp3: str = f'{file_path[:-4]}.mp3'
    wav_audio.export(file_path_mp3, format="mp3")
    data_audio: dict = {'file_id': record_id, 'file_path': file_path_mp3}
    add_file(db, data_audio)
    id_user: str = data_user['user_id']
    return {"message": f"http://{HOST}:{PORT}/record?id={record_id}&user={id_user}"} if record_id else None


def error_id_user_or_token_user(data_user: dict, db: Session) -> str | None:
    id_user: str = data_user['user_id']
    token_user: str | None = get_token(db, id_user)
    if not token_user:
        logger.error('Invalid user ID')
        return 'Invalid user ID'
    elif data_user['token'] != token_user:
        logger.error('Invalid Token')
        return 'Invalid Token'
    else:
        return None