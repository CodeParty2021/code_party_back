FROM python:3.9

WORKDIR /backend

SHELL ["/bin/bash", "-c"]

RUN apt-get update &

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \
  pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install

RUN echo "if [[ -z \"\${VIRTUAL_ENV}\" ]]; then" >> /root/.bashrc && \
  echo "source \$(pipenv --venv)/bin/activate" >> /root/.bashrc && \
  echo "fi"                                    >> /root/.bashrc