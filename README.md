# Transfer
## **Описание**

Проект реализующий выполнение задания "Задачка с переводом денег".

### **Используемые технологии:**
* PostgreSQL (хранилище данных)
* Django (веб-фреймворк)
* Swagger (документирование API)

## **Запросы**

* _**Зачислить/Списать средства:**_</br> 
**POST** запрос на end-point "/api/v1/user_transactions/" </br> параметры запроса: </br> "amount" - сумма (decimal, 2 знака после запятой); </br> "mark" - метка операции ("deposit" - поплнение, "withdraw" - списание). </br>


* _**Проверить баланс:**_ </br>
**GET** запрос на end-point "/api/v1/users/total/" </br>


* _**Детализация:**_ </br>
**GET** запрос на end-point "/api/v1/user_transactions/" </br>

## Примеры запросов (на локально запущенном сервере):

### Пополнение:
```curl
curl -X 'POST' \
  'http://127.0.0.1:8001/api/v1/user_transactions/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token db6a5ad43d9140d9fd19149836a479d957f459de' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": "1100.10",
  "mark": "deposit"
}'
```
Пример ответа:
```json
{
  "amount": "1100.10",
  "mark": "deposit",
  "created_at": "2023-08-29T21:38:23.622620Z"
}
```


### Списание:
```curl
curl -X 'POST' \
  'http://127.0.0.1:8001/api/v1/user_transactions/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token db6a5ad43d9140d9fd19149836a479d957f459de' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": "1100.10",
  "mark": "withdraw"
}'
```
Пример ответа:
```json
{
  "amount": "1100.10",
  "mark": "withdraw",
  "created_at": "2023-08-29T21:46:58.163700Z"
}
```


### Проверить баланс:
```curl
curl -X 'GET' \
  'http://127.0.0.1:8001/api/v1/users/total/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token db6a5ad43d9140d9fd19149836a479d957f459de'
```
Пример ответа:
```json
{
  "total": 0
}
```


### Посмотреть детализацию:
```curl
curl -X 'GET' \
  'http://127.0.0.1:8001/api/v1/user_transactions/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token db6a5ad43d9140d9fd19149836a479d957f459de'
```
Пример ответа:
```json
[
  {
    "amount": "1100.10",
    "mark": "withdraw",
    "created_at": "2023-08-29T21:46:58.163700Z"
  },
  {
    "amount": "1100.10",
    "mark": "deposit",
    "created_at": "2023-08-29T21:46:44.456764Z"
  }
]
```
