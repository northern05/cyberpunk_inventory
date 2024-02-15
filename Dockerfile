FROM python:3.10

WORKDIR /usr/src/app

# install dependencies
RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --force-reinstall -r requirements.txt


# Use in prod
COPY . /usr/src/app/

ARG LISTEN_PORT
ENV LISTEN_PORT=${LISTEN_PORT}
EXPOSE ${LISTEN_PORT}

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5000"]

