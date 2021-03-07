FROM python:3.8.7 AS compile-image

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install requests
RUN pip install click
RUN pip install pytest

FROM python:3.8.7-slim AS build-image
COPY --from=compile-image /opt/venv /opt/venv

ARG AppKey
ARG SecretKey
ARG SignKey

ENV AppKey=$AppKey
ENV SecretKey=$SecretKey
ENV SignKey=$SignKey
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
