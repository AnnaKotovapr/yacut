### Проект YaCut
### Описание
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
### Технологии
Python 3.7
Flask 2.0.2
### Инструкция по запуску
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AnnaKotovapr/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запуск:

```
flask run
```

### Примеры запросов
```
 Создание короткой ссылки:
 • Эндпоинт: /api/id/
 • Метод: POST
 • Описание: Создание короткой ссылки для предоставленной URL.
 • Пример тела запроса:json
```

Пример тела запроса:
```
{
    "url": "http://example.com",
    "custom_id": "custom123"
}
```

Образец ответа:
```
{
    "short_link": "http://localhost/custom1235",
    "url": "http://example.com"
}
```

```
Получить оригинальную ссылку по короткому идентификатору
• Метод: POST
• Эндпоинт: /api/id/{short_id}/

```

Пример запроса:
```
http://127.0.0.1:5000/api/id/ERVKWc/
```

Пример ответа:
```
{
    "url": "https://translate.yandex.ru/?source_lang=en&target_lang=ru&text=Error%3A%20While%20importing%20%27ya%20cut%27%2C%20an%20ImportError%20was%20raised."
}
```

### Авторы
Анна Котова
Telegram @annkotttt
