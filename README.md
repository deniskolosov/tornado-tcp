Простой TCP-сервер, принимающий сообщения от TCP-клиентов и отображающий их в веб-интерфейсе.

Для запуска нужен [Tornado](http://www.tornadoweb.org/en/stable/) и [Python 3](https://www.python.org/downloads/) 
#Установка и запуск:
```shell
git clone https://github.com/thefivekey/tornado-tcp.git
cd tornado-tcp/
pip install -r requirements.txt
python run app.py
```
Для тестирования можно в другом терминале запустить скрипт test.py, который сгенерирует сообщение в нужном формате.
```shell
python  test.py
```

