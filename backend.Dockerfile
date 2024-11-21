FROM python:3.10.4

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN python -m pip install -r requirements.txt
RUN playwright install

COPY ./backend ./backend

EXPOSE 8000

CMD ["python", "./backend/app/main.py"]