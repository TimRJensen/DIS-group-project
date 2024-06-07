FROM python:3.10-alpine

WORKDIR /app

# Project files
COPY requirements.txt .
COPY .env .
COPY ./src ./src

# Project dependencies
RUN pip install --upgrade pip \
    pip install -r requirements.txt

# Run 
CMD ["flask", "--app", "src/app.py", "run"]
