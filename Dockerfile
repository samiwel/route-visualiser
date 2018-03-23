FROM python:3

RUN apt update && apt install -y graphviz
RUN pip install pipenv

COPY . /app
WORKDIR /app
EXPOSE 5000

RUN pipenv install --deploy --system

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]