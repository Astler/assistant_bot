FROM python:3.8
LABEL maintainer="vladyclaw@gmail.com"
COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt
EXPOSE 49998
CMD ["python3", "-u", "app.py"]