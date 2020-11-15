FROM python:3.8-buster as builder

WORKDIR /opt/app
COPY Pipfile.lock /opt/app
RUN pip3 install pipenv && \
    pipenv install 

FROM python:3.8-slim-buster as runner

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

RUN apt update \
    && apt install -y libpq5 libxml2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -r -s /bin/false uvicorn

COPY deploy/uwsgi.ini /opt/app
COPY app /opt/app

USER uvicorn

EXPOSE 8000
CMD ["sleep", "infinity"]