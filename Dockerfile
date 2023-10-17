FROM python:3.10

RUN apt-get update && apt-get install -y \
    libncurses5

WORKDIR /app

COPY . /app

CMD [ "python", "bot.py" ]
