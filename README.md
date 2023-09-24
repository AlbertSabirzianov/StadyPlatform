# StadyPlatform
Тестовое задание от HardQode
Система для обучения
# Модели
Всего сушествует 4 модели, все находятся в приложении products
```commandline
Lesson - Сущность Урока,может находится в разных продуктах. 
```
```commandline
Availability - Сущность сохранения доступов к продукту. 
```
```commandline
Product - Сущность продукта.
```
```commandline
Result - Фиксатор времени и статуса просмотра урока.
```
# Эндпоинты
```commandline
POST /api-token-auth/
```
Получение токена авторизации
```commandline
GET /api/lessons/
```
API Для выведения списка всех уроков по всем продуктам к которым пользователь имеет доступ.
```commandline
GET /api/products/<product_id>/lessons/
```
API Для выведения спискауроков по конкретному продукту к которому пользователь имеет доступ. (Если пользователь не
имеет доступ к продукту придёт ответ 403 FORBIDDEN)
```commandline
GET /api/products/
```
API отображения статистики по всем продуктам.

# Установка
Скачайте репозиторий на свой компьютер
```commandline
git clone https://github.com/AlbertSabirzianov/StadyPlatform.git
```
Передите в директорию проекта
```commandline
cd StadyPlatform/StadyPlatform
```
Установите зависимости
```commandline
pip install requirements.txt
```
Запустите миграции
```commandline
python manage.py migrate
```
Загрузите тестовые данные
```commandline
python manage.py data_to_db
```
Запустите сервер
```commandline
python manage.py runserver
```
# Внимание!
Все эндпоинты подразумевают допуск только авторизированным пользователям, 
поэтому перед использованием вам необходимо получить токен и вставлять его в 
header каждого запроса. Если вы загрузили тестовые данные командой python manage.py data_to_db,
то можете использовать
двух готовых юзеров:

```json
[
  {
  "username": "al",
  "password": "123"
  },
  {
  "username": "ken",
  "password": "321"
  }
]
```