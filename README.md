# Transfer
## **Описание**

Проект реализующий выполнение задания "Задачка с переводом денег".

### **Используемые технологии:**
* PostgreSQL (хранилище данных)
* Django (веб-фреймворк)
* Swagger (документирование API)

## **Запросы**

* _**Получить свой ID:**_</br> 
**GET** запрос на end-point "/api/v1/users/me/" </br>


* _**Проверить баланс:**_ </br>
**GET** запрос на end-point "/api/v1/users/total/" </br>


* _**Перевод средств:**_</br> 
**POST** запрос на end-point "/api/v1/user_transactions/" </br> параметры запроса: </br> "recipient" - ID пользователя которому переводим средства; </br> "amount" - сумма (decimal, 2 знака после запятой). </br>


* _**Детализация:**_ </br>
**GET** запрос на end-point "/api/v1/user_transactions/" </br> в ответе будет содержаться тип транзакции для конкретного пользователя: deposit(пополнение) или withdraw(списание)

## Примеры запросов (на локально запущенном сервере):

### Получить свой ID:
```curl
curl -X 'GET' \
  'http://127.0.0.1:8001/api/v1/users/me/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token db6a5ad43d9140d9fd19149836a479d957f459de'
```
Пример ответа:
```json
{
  "id": 1,
  "email": "first@user.com"
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
  "total": 10000
}
```


### Перевод средств:
```curl
curl -X 'POST' \
  'http://127.0.0.1:8001/api/v1/user_transactions/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token db6a5ad43d9140d9fd19149836a479d957f459de' \
  -H 'Content-Type: application/json' \
  -d '{
  "recipient": 2,
  "amount": "0.01"
}'
```
Пример ответа:
```json
{
  "recipient": 2,
  "amount": "0.01",
  "created_at": "2023-08-30T20:56:34.712763Z"
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
    "amount": "0.01",
    "created_at": "2023-08-30T20:56:34.712763Z",
    "transaction_type": "withdraw"
  },
  {
    "amount": "10000.00",
    "created_at": "2023-08-30T20:44:59.235178Z",
    "transaction_type": "deposit"
  }
]
```
