FROM python:3.10.4

WORKDIR /usr/src/app

COPY ./backend/app/requirements.txt .

RUN python -m pip install -r requirements.txt

COPY ./backend ./backend

EXPOSE 8000

CMD ["python", "./backend/app/main.py"]