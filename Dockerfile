FROM chambm/pwiz-skyline-i-agree-to-the-vendor-licenses:latest

LABEL authors="Paul Benton <paul.benton@vicinitas.com>"
LABEL version="1.0.0"
LABEL description="API into running msconvert.exe to convert vendor files to mzML"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    pip

RUN pip install --upgrade pip
RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

RUN pip install python-multipart
COPY . /app
EXPOSE 8000

CMD [ "uvicorn",  "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]

