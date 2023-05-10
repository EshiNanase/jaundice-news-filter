# Фильтр желтушных новостей

[TODO. Опишите проект, схему работы]

Пока поддерживается только один новостной сайт - [ИНОСМИ.РУ](https://inosmi.ru/). Для него разработан специальный адаптер, умеющий выделять текст статьи на фоне остальной HTML разметки. Для других новостных сайтов потребуются новые адаптеры, все они будут находиться в каталоге `adapters`. Туда же помещен код для сайта ИНОСМИ.РУ: `adapters/inosmi_ru.py`.

В перспективе можно создать универсальный адаптер, подходящий для всех сайтов, но его разработка будет сложной и потребует дополнительных времени и сил.

# Как установить

Вам понадобится Python версии 3.7 или старше. Для установки пакетов рекомендуется создать виртуальное окружение.

Первым шагом установите пакеты:

```python3
pip install -r requirements.txt
```

# Как запустить

```python3
python server.py
```

У вас запустится сервер на http://127.0.0.1:8080

# Как работать

Вы можете узнавать о степени желтушности статьи с сайта Inosmi.ru по ссылке сверху с дополнительным параметром urls

Например:
```python3
http://127.0.0.1:8080/?urls=https://inosmi.ru/20230510/karlson-262806210.html
```

В ответ вы получите ответ в JSON-формате.

Например:
```python3
{"0": {"url": "https://inosmi.ru/20230510/karlson-262806210.html", "word_count": 397, "score": 1.77, "status": "OK"}}
```

В случае, если вы хотите узнать о степени желтушности несколько статей, то перечислите их через запятую

Например:
```python3
http://127.0.0.1:8080/?urls=https://inosmi.ru/20230510/karlson-262806210.html,https://inosmi.ru/20230510/sdelka-262821054.html
```


# Как запустить тесты

Для тестирования используется [pytest](https://docs.pytest.org/en/latest/), тестами покрыты фрагменты кода сложные в отладке: text_tools.py и адаптеры. Команды для запуска тестов:

```
python -m pytest adapters/inosmi_ru.py
```

```
python -m pytest text_tools.py
```
```
python -m pytest process_article_tests.py
```
