                                                                                                                                                                                                                                                    FROM python:3.8.10

RUN apt-get update

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt



COPY . .

WORKDIR /app


ADD . /app


CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT