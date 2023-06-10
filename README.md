Инструкция. 
1. Скачать проект на локальную машину
2. запустить docker-compose build
3. запустить docker-compose up

Примеры запросов:

```
async def test_add_user():
    async with httpx.AsyncClient() as client:
        r = await client.post('http://0.0.0.0:8000/users', json={'name': 'test'})
    return r.json() 
 ```
    
print(asyncio.run(test_add_user()))

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
