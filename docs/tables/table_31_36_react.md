# Таблица 31 – Структура проекта React

| Каталог/файл | Назначение |
|---|---|
| components | React-компоненты приложения |
| pages | Страницы приложения |
| services | Работа с REST API |
| contexts | Хранение состояния авторизации |
| index.css | Глобальные стили приложения |
| App.js | Корневой компонент |
| index.js | Точка входа приложения |

---

# Таблица 32 – Основные React-компоненты приложения

| Компонент | Назначение |
|---|---|
| Home | Отображение каталога товаров |
| Profile | Редактирование профиля пользователя |
| Login | Авторизация пользователя |
| Register | Регистрация пользователя |
| Cart | Управление корзиной |
| Orders | Просмотр заказов пользователя |

---

# Таблица 33 – Маршрутизация приложения

| Маршрут | Компонент |
|---|---|
| / | Home |
| /profile | Profile |
| /login | Login |
| /register | Register |
| /cart | Cart |
| /orders | Orders |

---

# Таблица 34 – Архитектура взаимодействия React с API

| Компонент | Файл | Роль во взаимодействии с API |
|---|---|---|
| apiClient (Axios instance) | services/api.js | Единая точка выхода всех HTTP-запросов. Содержит baseURL, заголовки по умолчанию и два interceptor |
| Request Interceptor | services/api.js | Перед каждым запросом читает access-токен из localStorage и добавляет заголовок Authorization: Bearer <token>. Если токена нет — запрос идёт без заголовка (публичный доступ) |
| Response Interceptor | services/api.js | При получении HTTP 401 автоматически выполняет POST /api/auth/token/refresh/, обновляет access-токен в AuthContext и повторяет исходный запрос. При ошибке refresh — перенаправляет на /login |
| AuthContext | contexts/AuthContext.jsx | Хранит состояние авторизации (user, loading); сами токены хранятся в localStorage. Предоставляет методы login(), logout(). Доступен любому компоненту через хук useAuth() |
| Вызовы API | services/api.js | Компоненты обращаются к REST API напрямую через экземпляр apiClient методами api.get(), api.post(), api.patch(), api.delete(). Запросы выполняются внутри хуков useEffect и обработчиков событий. |
| PrivateRoute | components/PrivateRoute.jsx | HOC-компонент, проверяющий наличие авторизации. Если пользователь не авторизован — перенаправляет на /login. Обёртывает маршруты /cart, /orders, /profile |

---

# Таблица 35 – Инструменты статического анализа кода

| Инструмент | Назначение |
|---|---|
| flake8 | Анализ качества Python-кода |
| ESLint | Анализ качества JavaScript-кода |
| Prettier | Форматирование JavaScript-кода |

---

# Таблица 36 – Методы оптимизации запросов ORM

| Метод | Назначение |
|---|---|
| select_related() | Оптимизация связей ForeignKey |
| prefetch_related() | Оптимизация связей Many-to-Many и обратных связей |
