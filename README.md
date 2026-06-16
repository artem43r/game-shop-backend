# Game Shop — Backend

REST API для магазина игровой валюты. Курсовой проект по дисциплине «Технология разработки программного обеспечения», траектория Б.

## Стек технологий

- Python 3.14.3 / Django 6.0.5
- Django REST Framework 3.17.1
- SimpleJWT — аутентификация (access + refresh токены)
- PostgreSQL — база данных
- drf-spectacular — документация API (Swagger)
- django-cors-headers — поддержка CORS для React-фронтенда

## Установка и запуск

```bash
# 1. Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Создать файл .env по образцу .env.example и заполнить настройки БД

# 4. Применить миграции
python manage.py migrate

# 5. Создать суперпользователя
python manage.py createsuperuser

# 6. Запустить сервер
python manage.py runserver
```

Swagger UI доступен по адресу: http://localhost:8000/api/docs/

## Структура проекта

```
game-shop-backend/
├── config/          # Настройки Django (settings, urls, wsgi)
├── users/           # Пользователи, JWT-аутентификация, профиль
├── shop/            # Категории и товары (игровая валюта)
├── orders/          # Корзина и заказы
├── manage.py
├── requirements.txt
└── .env.example
```

## API эндпоинты

### Аутентификация
| Метод | Эндпоинт | Доступ | Описание |
|-------|----------|--------|----------|
| POST | /api/auth/register/ | Все | Регистрация |
| POST | /api/auth/login/ | Все | Получение JWT-токенов |
| POST | /api/auth/token/refresh/ | Все | Обновление access-токена |
| POST | /api/auth/logout/ | Авторизованные | Выход, инвалидация refresh-токена |
| GET | /api/auth/profile/ | Авторизованные | Просмотр профиля |
| PUT/PATCH | /api/auth/profile/ | Авторизованные | Обновление профиля |

### Магазин
| Метод | Эндпоинт | Доступ | Описание |
|-------|----------|--------|----------|
| GET | /api/categories/ | Все | Список категорий |
| GET | /api/products/ | Все | Список товаров |
| GET | /api/products/?search=... | Все | Поиск по товарам |
| GET | /api/products/?category=1 | Все | Фильтр по категории |
| POST | /api/products/ | Админ | Создание товара |
| PUT/PATCH | /api/products/{id}/ | Админ | Редактирование товара |
| DELETE | /api/products/{id}/ | Админ | Удаление товара |

### Корзина и заказы
| Метод | Эндпоинт | Доступ | Описание |
|-------|----------|--------|----------|
| GET | /api/cart/ | Авторизованные | Просмотр корзины |
| POST | /api/cart/ | Авторизованные | Добавить товар в корзину |
| PATCH | /api/cart/items/{id}/ | Авторизованные | Изменить количество |
| DELETE | /api/cart/items/{id}/ | Авторизованные | Удалить из корзины |
| GET | /api/orders/ | Авторизованные | Список заказов |
| POST | /api/orders/ | Авторизованные | Оформить заказ из корзины |
| GET | /api/orders/{id}/ | Авторизованные | Детали заказа |
| PATCH | /api/orders/{id}/ | Админ | Изменить статус заказа |

## Разграничение доступа

| Уровень | Роль | Возможности |
|---------|------|-------------|
| 1 | Гость | Просмотр категорий и товаров |
| 2 | Авторизованный пользователь | + корзина, заказы, профиль |
| 3 | Администратор (is_staff) | + управление товарами и категориями, смена статусов заказов |

## Статистика разработки


- Всего коммитов: 16
- Период разработки: 21.05.2026 — 04.06.2026
- Средняя частота: 6 коммитов/неделю

### Диаграммы

Основные диаграммы (IDEF0, Use Case, Domain Model, ER-диаграмма) приведены в пояснительной записке к курсовому проекту.

| Диаграмма | Файл |
|---|---|
| Бизнес-прецеденты (BUC) | [diagram_02_buc.puml](docs/diagrams/diagram_02_buc.puml) |
| Диаграмма компонентов | [diagram_05_components.puml](docs/diagrams/diagram_05_components.puml) |
| Схема JWT-аутентификации | [diagram_06_jwt_sequence.puml](docs/diagrams/diagram_06_jwt_sequence.puml) |
| Последовательность авторизации | [diagram_08_auth_sequence.puml](docs/diagrams/diagram_08_auth_sequence.puml) |
| Последовательность работы с товаром | [diagram_09_product_sequence.puml](docs/diagrams/diagram_09_product_sequence.puml) |
| Диаграмма классов | [diagram_10_classes.puml](docs/diagrams/diagram_10_classes.puml) |
| Диаграмма Ганта | [diagram_11_gantt.jpg](docs/diagrams/diagram_11_gantt.jpg) |

### Таблицы

Основные таблицы (Паспорт проекта, Матрица стейкхолдеров, SWOT-анализ, Спецификации прецедентов, Глоссарий, Бизнес-правила, Физическая модель данных, Эндпоинты API, Параметры JWT, Роли доступа, Результаты тестирования) приведены в пояснительной записке.

Вспомогательные таблицы вынесены в папку [docs/tables/](docs/tables/):

| Таблица | Файл |
|---|---|
| Таблица 3 — Бизнес-прецеденты системы (BUC) | [table_03_buc.md](docs/tables/table_03_buc.md) |
| Таблица 5 — Сравнение подходов к разработке | [table_05_comparison.md](docs/tables/table_05_comparison.md) |
| Таблицы 6–7 — ROI и затраты на разработку | [table_06_07_roi.md](docs/tables/table_06_07_roi.md) |
| Таблица 13 — Атрибуты сущностей предметной области | [table_13_attributes.md](docs/tables/table_13_attributes.md) |
| Таблицы 15–16, 18 — Архитектурные решения и паттерны | [table_15_16_18_architecture.md](docs/tables/table_15_16_18_architecture.md) |
| Таблицы 19–22 — Структура проекта Django и ORM | [table_19_22_structure.md](docs/tables/table_19_22_structure.md) |
| Таблицы 25–28 — Потоки JWT-аутентификации | [table_25_28_jwt_flows.md](docs/tables/table_25_28_jwt_flows.md) |
| Таблицы 31–36 — React: компоненты, маршруты, оптимизация | [table_31_36_react.md](docs/tables/table_31_36_react.md) |
| Таблицы 41–46 — Установка, конфигурация, управление проектом | [table_41_46_management.md](docs/tables/table_41_46_management.md)

### Листинги кода (Приложение А)

**А.1 — Модели данных (Django ORM)**

| Файл | Ссылка |
|---|---|
| users/models.py — модель User (AbstractUser) | [строки 1–23](https://github.com/artem43r/game-shop-backend/blob/main/users/models.py#L1-L23) |
| shop/models.py — модели Category и Product | [строки 1–41](https://github.com/artem43r/game-shop-backend/blob/main/shop/models.py#L1-L41) |
| orders/models.py — Cart, CartItem, Order, OrderItem | [строки 1–125](https://github.com/artem43r/game-shop-backend/blob/main/orders/models.py#L1-L125) |

**А.2 — Сериализаторы (Django REST Framework)**

| Файл | Ссылка |
|---|---|
| shop/serializers.py — ProductSerializer | [строки 16–30](https://github.com/artem43r/game-shop-backend/blob/main/shop/serializers.py#L16-L30) |
| orders/serializers.py — OrderSerializer | [строки 57–63](https://github.com/artem43r/game-shop-backend/blob/main/orders/serializers.py#L57-L63) |

**А.3 — React-компоненты (фронтенд)**

| Файл | Ссылка |
|---|---|
| AuthContext.jsx — управление JWT | [строки 1–65](https://github.com/artem43r/game-shop-frontend/blob/main/src/contexts/AuthContext.jsx#L1-L65) |
| Cart.jsx — корзина и оформление заказа | [src/pages/Cart.jsx](https://github.com/artem43r/game-shop-frontend/blob/main/src/pages/Cart.jsx) |