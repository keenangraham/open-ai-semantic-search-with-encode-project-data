FROM --platform=linux/amd64 python:3.10.11-buster

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv

RUN useradd -u 1444 -m python

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    git

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN chown -R python:python $VIRTUAL_ENV

WORKDIR /scripts

COPY --chown=python:python scripts .

RUN chmod -R +x /scripts

WORKDIR /data

COPY --chown=python:python /data .

WORKDIR /ssed

COPY --chown=python:python /backend/setup.cfg /backend/pyproject.toml ./

COPY --chown=python:python /backend/src/ssed/__init__.py src/ssed/__init__.py

USER python

RUN python -m pip install --upgrade pip

RUN pip install -e .[test]

COPY --chown=python:python /backend .

EXPOSE 8000

ENTRYPOINT ["/scripts/entrypoint.sh"]

CMD ["/scripts/run-api.sh"]