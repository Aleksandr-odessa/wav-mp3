# Проект "wav to mp3"

Проект выполнен на языке Python v.3.10.6 и фреймворка FastAPI.
## Сборка контейнера docker compose
```
docker-compose build
```
### Запуск контейнера 
```
docker-compose up
```

### Пример CURL POST запроса:

Request URL
http://0.0.0.0:8000/users

```
curl -X 'POST' \
  'http://0.0.0.0:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "name"
}'
```
Ответ:\
Server response 201 

Response body
```
{
  "user_id": "68f60265-1969-4e9c-900d-2b2fb02bcba2",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoiU2FzYSJ9.JIEtt6WkUxHbFNL4pb07ICemeLUCHaHf62l0wRshWfE"
}
```

Пример CURL POST запроса:

Request URL
http://0.0.0.0:8000/users/wav
 
```
curl -X 'POST' \
  'http://0.0.0.0:8000/users/wav' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'audio_file=@sample-3s.wav;type=audio/wav' \
  -F 'data={   "user_id": "68f60265-1969-4e9c-900d-2b2fb02bcba2",   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoiU2FzYSJ9.JIEtt6WkUxHbFNL4pb07ICemeLUCHaHf62l0wRshWfE" }'
```
Ответ:\
Server response 201 

Response body:

"http://0.0.0.0:8000/record?id=2859c7f4-5610-48d2-9d0b-3c66a31ad7bb&user=68f60265-1969-4e9c-900d-2b2fb02bcba2"
