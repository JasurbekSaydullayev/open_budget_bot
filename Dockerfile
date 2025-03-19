FROM python:3.11

WORKDIR /app

COPY req.txt .
COPY entrypoint.sh .
COPY . .

RUN pip install --no-cache-dir -r req.txt
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
