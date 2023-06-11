# Проект Wav to Mp3

Проект представляет собой веб-сервис, выполняющий следующие функции:
    1. Создание пользователя;
    2. Для каждого пользователя - сохранение аудиозаписи в формате wav, преобразование её в формат mp3 и запись в базу данных и предоставление ссылки для скачивания аудиозаписи.

Сервис принимает на вход запросы с именем пользователя, создаёт в базе данных, пользователя заданным именем, так же генерирует уникальный идентификатор пользователя и UUID токен доступа (в виде строки) для данного пользователя и возвращает сгенерированные идентификатор пользователя и токен.
В случае если пользователь новый (в бд его не было) будет отправлен  код 201("Создано") и json с id пользователя token доступ.  В случае если пользователь с таким именем уже существует будет отправлен код 200 ("ОК") и сообщение {"error_name": "user with name already is"}

Для добавление аудиозаписи, сервис принимает на вход запросы, содержащие уникальный идентификатор пользователя, токен доступа и аудиозапись в формате wav ( при этом происходит проверка на правльный идентификатор пользователя, токен доступа и уникальность отсутствие файла  стаким названием в БД, преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет их в базе данных.
Результатом работы сервиса является ссылка вида http://host:port/record?id=id_записи&user=id_пользователя на скачивание файла в сормате мр3


Проект можно собрать с помощью docker compose. 
Для этого необходимо:
1. Склонировать либо скачать проект ("Code" -> "Local" -> "Dowload ZIP" либо  "HTTPS" либо "GitHubCLI")
2. На локальной машине установить Docker и Docker-compose (если они еще не установлены)
3. В терминале перейти в папку в которой находится скачаный проект
4. Собрать образ - docker-compose build
5. Запустить контейнеры командой -docker-compose up


Примеры запросов:

```
async def test_add_user():
    async with httpx.AsyncClient() as client:
        r = await client.post('http://0.0.0.0:8000/users', json={'name': 'test'})
    return r.json() 

print(asyncio.run(test_add_user()))
```

id = 'id user полученный в ответ на запрос 'http://0.0.0.0:8000/users', json={'name': 'test'}
access_token = 'token полученный в ответ на запрос 'http://0.0.0.0:8000/users', json={'name': 'test'}

file_path = путь расположения файла
```
def upload_audio(id, access_token, file_path):
    url = "http://0.0.0.0:8000/users/wav"
    files = {"audio_file": open(file_path, "rb")}
    data = {"data": json.dumps({"user_id": id, "access_token": access_token})}
    response = httpx.post(url, data=data, files=files)
    return response.text
```
print(upload_audio(id, access_token, file_path))