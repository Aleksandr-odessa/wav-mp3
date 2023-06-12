# Проект "Викторина"
Проект представляет собой сервис POST REST метод, принимающий на вход запросы с содержимым вида {"questions_num": integer}. После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов. Полученные ответы сохраняться в базе данных PostgreSQL (развернутой из docker образа).В случае, если в БД имеется такой же вопрос, к публичному API с викторинами  выполняються дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины. Ответом на запрос  является предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.

Проект выполнен на языке Python v.3.10.6 и фреймворка FastAPI.

Проект можно собрать с помощью docker compose. 
Для этого необходимо:
1. Склонировать либо скачать проект ("Code" -> "Local" -> "Dowload ZIP" либо  "HTTPS" либо "GitHubCLI")
2. На локальной машине установить Docker и Docker-compose (если они еще не установлены)
3. В терминале перейти в папку в которой находится скачаный проект
4. Собрать образ - docker-compose build
5. Запустить контейнеры командой -docker-compose up

Пример CURL POST запроса:
Request URL
http://0.0.0.0:8000/users

curl -X 'POST' \
  'http://0.0.0.0:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "name"
}'
Ответ:
Server response 201 

Response body
{
  "user_id": "68f60265-1969-4e9c-900d-2b2fb02bcba2",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoiU2FzYSJ9.JIEtt6WkUxHbFNL4pb07ICemeLUCHaHf62l0wRshWfE"
}


Пример CURL POST запроса:
Request URL
http://0.0.0.0:8000/users/wav
 
curl -X 'POST' \
  'http://0.0.0.0:8000/users/wav' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'audio_file=@sample-3s.wav;type=audio/wav' \
  -F 'data={   "user_id": "68f60265-1969-4e9c-900d-2b2fb02bcba2",   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoiU2FzYSJ9.JIEtt6WkUxHbFNL4pb07ICemeLUCHaHf62l0wRshWfE" }'

Ответ:
Server response 201 

Response body
"http://0.0.0.0:8000/record?id=2859c7f4-5610-48d2-9d0b-3c66a31ad7bb&user=68f60265-1969-4e9c-900d-2b2fb02bcba2"