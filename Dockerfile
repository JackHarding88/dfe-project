FROM python:3.6-alpine

EXPOSE 5000

WORKDIR /app
ENV SQLALCHEMY_DATABASE_URI="sqlite:///data.db"

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT python app.py
