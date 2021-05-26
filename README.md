# Stress bot

Stress bot is a Telegram bot for practicticing Russian language word stress rules.

Tested on Python 3.8.5

![Game](https://user-images.githubusercontent.com/43320720/119373638-4bb81f80-bcc1-11eb-9ce4-40f23355858c.png)

![Rating](https://user-images.githubusercontent.com/43320720/119626096-88942b80-be13-11eb-89c3-391c70b2fef2.png)

![Settings](https://user-images.githubusercontent.com/43320720/119626100-89c55880-be13-11eb-86ed-ae01e1ebde56.png)

## Running

1. Create new Python venv and install requirements.
```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

2. Set your Telegram bot token in `config.py`

3. Create database
```
alembic upgrade head
```
3. Run
```
python3 main.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Used libraries

* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [sqlalchemy](https://www.sqlalchemy.org/)
