FROM python:3.6-buster

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN apt update
RUN apt install -y python3 python3-pip openssl ca-certificates python3-openssl wget bash linux-headers-amd64
# RUN apt install libc6-compat linux-pam libxml2 libstdc++
# RUN apt install libffi-dev openssl-dev python-dev py-pip build-base \&&
RUN pip install --upgrade pip \
  && pip install --upgrade pipenv\
  && pip install --upgrade -r /tmp/requirements.txt
  # && apk del build-dependencies

COPY . /app
ENV FLASK_APP=server/__init__.py
CMD ["python", "manage.py", "start", "0.0.0.0:3000"]
