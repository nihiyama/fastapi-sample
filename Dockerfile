FROM python:3.8-buster as builder

COPY Pipfile.lock /opt/app/
WORKDIR /opt/app/
RUN pip3 install pipenv && \
    pipenv sync --system 

FROM python:3.8-slim-buster as runner

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=builder /usr/local/bin/alembic /usr/local/bin/alembic

RUN apt update \
    && apt install -y libpq5 libxml2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -r -s /bin/false uvicorn

COPY app /opt/app

USER uvicorn
WORKDIR /opt/app/

EXPOSE 8000
CMD ["sleep", "infinity"]