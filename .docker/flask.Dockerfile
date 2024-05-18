FROM python:3.10-alpine

WORKDIR /src

# Project files
COPY requirements.txt /src
COPY .env /src
COPY ./src /src

# Project dependencies
RUN pip install --upgrade pip \
    pip install -r requirements.txt

# Run 
CMD ["flask", "run"]