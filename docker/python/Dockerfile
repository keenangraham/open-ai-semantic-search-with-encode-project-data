FROM python:3.10.11-buster

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

WORKDIR /python

COPY --chown=python:python requirements.txt requirements.txt

USER python

RUN echo $(ls)

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

ENTRYPOINT ["/docker/entrypoint.sh"]