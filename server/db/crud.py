from db.schemas import Users, Audio


def add_user_to_db(users: dict, db) -> None:
    user = Users(id_user=users["user_id"], name=users["user_name"], token=users["token"])
    db.add(user)
    db.commit()
    db.refresh(user)


def get_user(user: str, db) -> bool | None:
    if db.query(Users).filter(Users.name == user).first():
        return True


def get_id(db, id_user) -> dict | None:
    token = db.query(Users).filter(Users.id_user == id_user).first()
    if token:
        return {'token': token.token, 'name': token.name}


def add_file(db, audio: dict) -> None:
    files = Audio(file_id=audio['file_id'], audio_file=audio['file_path'])
    db.add(files)
    db.commit()


def get_mp3(db, id_file) -> str:
    path_file = db.get(Audio, id_file)
    return path_file.audio_file
