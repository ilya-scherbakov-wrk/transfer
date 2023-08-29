# Transfer
**Описание**

Проект реализующий выполнение задания "Задачка с переводом денег".

**Запросы**

* _**Зачислить/Списать средства:**_</br> 
**POST** запрос на end-point "/api/v1/user_transactions/" </br> параметры запроса: </br> "user" - id юзера; </br> "amount" - сумма (decimal, 2 знака после запятой); </br> "mark" - метка операции ("deposit" - поплнение, "withdraw" - списание). </br>
* _**Проверить баланс:**_ </br>
**GET** запрос на end-point "/api/v1/users/<user_id>/total/" </br>
* _**Детализация:**_ </br>
**GET** запрос на end-point "/api/v1/users/<user_id>/story/" </br>

**CURL примеры запросов на локально запущенном сервере:** </br>
Все примеры выполнены для пользователя с id 1.
* _**Пополнить на 1100.10:**_ </br>
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/user_transactions/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user": 1,
  "amount": "1100.10",
  "mark": "deposit"
}'
* _**Списать 100.10:**_ </br>
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/user_transactions/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user": 1,
  "amount": "100.10",
  "mark": "withdraw"
}'
* _**Проверить баланс:**_ </br>
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/users/1/total/' \
  -H 'accept: application/json'
* _**Посмотреть детализацию:**_ </br>
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/users/1/story/' \
  -H 'accept: application/json'
