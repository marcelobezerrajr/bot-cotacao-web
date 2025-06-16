FROM botcity/botcity-python-web-chrome:latest

WORKDIR /botcity

RUN apt-get update && apt-get install -y python3-venv && rm -rf /var/lib/apt/lists/*

COPY . .

RUN python -m venv venv

RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

CMD ["./venv/bin/python", "bot.py"]
