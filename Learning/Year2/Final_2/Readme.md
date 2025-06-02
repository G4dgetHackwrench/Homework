# Сервис рекомендаций

### 1. Описание проекта

Сервис выдаёт рекомендации по идентификатору пользователя.

Ожидает 4 файла формата csv следующей структуры:

1. **Лог событий(events)**
	* timestamp — время события(int64)
	* visitorid — идентификатор пользователя(int64)
	* event — тип события(object)
	* itemid — идентификатор объекта(int64)
	* transactionid — идентификатор транзакции, если она проходила(float64)

2. **Дерево категорий(category_tree)**
	* category_id — идентификатор категорий(int64)
	* parent_id — идентификатор родительской категории(float64)

3. **Свойства товаров(item_properties_part1)**
4. **Свойства товаров(item_properties_part2)**
	* timestamp — момент записи значения свойства(int64)
	* item_id — идентификатор объекта(int64)
	* property — свойство(захешировано, object)
	* value — значение свойства(object)

Ссылки на скачивание: [Лог событий](https://drive.google.com/file/d/1brIA9_FJOFQm4WkI1_LXMjPP_fNtN6rC/view), [Дерево категорий](https://drive.google.com/file/d/1TYhW6Y8F3C7ozC7rN-K5M7tVpvI3gm-7/view), [Свойства товаров часть1](https://drive.google.com/file/d/1TPW28LINiGJ5PsisoHyhNk0uxUxb9h6W/view), [Свойства товаров часть2](https://drive.google.com/file/d/1F4rgCH7JHJBpXP4DYEcYTqlq3DxXF2pc/view)

### 2. Преобразование данных

Все таблицы объединены в одну и добавлены новые признаки, итоговую таблицу можно скачать по [ссылке](https://drive.google.com/file/d/117f5IZIs5phJasxYdPP1UwGONBv--HmU/view?usp=drive_link).

**Добавленные признаки:**

* date, day, weekend, timeday, minute, dayofweek, month

* target(целевой признак, купил или добавил в корзину - 1, просмотр - 0)

* Признаки для товаров: признаки с некоторыми популярными свойствами(есть это свойство у товара или нет), 'categoryid', 'nesting', 'categoryid_enc', 'itemid_day', 'itemid_weekend', 'itemid_timeday', 'item_count', 'item_purchase_count', 'item_mean', 'item_days_since_last_view', 'category_popularity', 'category_popularity_purchase', 'category_avg_conversion', 'category_unique_items', 'item_unique_users', 'item_returning_users_ratio', 'item_recent_7d', 'item_recent_7d_purchase', 'item_recent_30d', 'item_recent_30d_purchase', 'item_days_since_last_purchase'

* Признаки для пользователей: 'visitorid_day', 'visitorid_weekend', 'visitorid_timeday', 'visitorid_categoryid', 'visitorid_categoryid_enc', 'user_count', 'user_purchase_count', 'user_mean', 'user_avg_time_between_actions', 'user_repeat_view_ratio', 'user_activity_trend'

### 3. Валидация

Для валидации отобраны пользователи, которые встречаются не менее 5 раз в датасете и совершили хотя бы 1 покупку. Для тестового датасета отобраны последние(по дате) 30% взаимодействий.
### 4. Эксперименты

Random_state = 19

Гиперпараметры подбираются с помощью библиотеки Optuna

**Базовая модель:**

* Модель ALS из библиотеки Implicit
* Гиперпараметры:

	{factors=200, regularization=0.01,

	iterations=15, 

	calculate_training_loss=True, 

	num_threads=4}

* Precision@3 = 14%

Также были опробованы **XGBoost**(классификатор), **LightFM**(классификатор) с подбором гиперпараметров, значения Precision@3 не превышали 15%.

**Итоговая модель**

1. Для кандидатогенератора используется модель **ALS** с подобранными гиперпараметрами:

	{'factors': 148,

	'regularization': 0.02205850352887652,

	'alpha': 13.526664255279133,

	'iterations': 40}
	
	Значение метрики **Recall@20 = 23,6%**

2. Для ранжирования используется **LGBMRanker** с подобранными гиперпараметрами:

	{'scale_pos_weight': 32.76646433606382,

	'num_leaves': 68,

	'learning_rate': 0.13252142979294942,

	'n_estimators': 295,

	'min_child_samples': 12,

	'max_depth': 8,

	'reg_alpha': 1.3583072289221058e-09,

	'reg_lambda': 0.04857113119670418,

	'subsample': 0.948178146926568,

	'colsample_bytree': 0.9433960599960594,

	'lambdarank_truncation_level': 9}
	
	Значение метрики **Precision@3 = 25%** при n=5(10 кандидатов)

### 4. Запуск сервиса

#### 1. Общая структура:

	---app/
	|	|--- models
	|	|    |--- final_als.pkl    # Модель кандидатогенератора
	|	|    |--- final_rr.pkl     # Модель реранкера
	|	|--- templates
	|	|    |--- docs.html        # Фронт документации
	|	|    |--- index.html       # Фронт главной страницы
	|	|--- __init__.py
	|	|--- main.py               # Основное приложение
	|	|--- model.py              # Модель рекомендаций
	|	|--- metrics.py            # Логика метрик
	|	|--- Readme.md             # Документация  
	---requirements.txt            # Зависимости
	---Dockerfile                   # Конфигурация Docker


Метод GET	/	Главная страница с интерфейсом тестирования

Метод GET	/docs	Документация сервиса

Метод GET	/recommend/<int:user_id>	Получение рекомендаций для пользователя


#### 2. Сборка Docker-образа:
```
docker build -t recommendation_service .
```

#### 3. Запуск контейнера:
```
docker run -d -p 5000:5000 --name rec_service recommendation_service
```

#### 4. Команды для управления сервисом:

Запуск
```
docker run -d -p 5000:5000 --name rec-service recommendation-service
```
Остановка
```
docker stop rec-service
```
Перезапуск
```
docker restart rec-service
```
Просмотр логов
```
docker logs rec-service
```
Войти внутрь контейнера
```
docker exec -it rec-service bash
```
Рекомендации внутри контейнера
```
curl localhost:5000/recommend/1
```
Выйти из контейнера
```
exit
```
Удаление контейнера
```
docker rm rec-service
```

#### 5. Получение рекомендаций:
```
curl http://localhost:5000/recommend/123
```

#### 6. Проверка метрик:
```
curl http://localhost:5000/metrics
```
Сервис предоставляет метрики в формате Prometheus для мониторинга производительности и анализа работы API.

* 'http_requests_total' счетчик запросов
```
http_requests_total{method="GET", endpoint="/recommend/123", http_status="200"} 42
```
* 'http_request_latency_seconds' время выполнения запросов
```
http_request_latency_seconds_bucket{method="GET", endpoint="/recommend/123", le="0.5"} 38
http_request_latency_seconds_sum{method="GET", endpoint="/recommend/123"} 12.45
http_request_latency_seconds_count{method="GET", endpoint="/recommend/123"} 42
```
#### 7. Документация:
```
curl http://localhost:5000/docs
```