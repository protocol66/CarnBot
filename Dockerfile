FROM python:3

WORKDIR /

RUN git clone https://github.com/protocol66/CarnBot
WORKDIR /CarnBot

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "CarnBot.py" ]