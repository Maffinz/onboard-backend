FROM python:3.6-buster

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN apt update
RUN apt install -y python3 python3-pip openssl ca-certificates python3-openssl wget bash linux-headers-amd64
# RUN apt install libc6-compat linux-pam libxml2 libstdc++
# RUN apt install libffi-dev openssl-dev python-dev py-pip build-base \&&
RUN pip3 install --upgrade pip \
  && pip3 install --upgrade pipenv\
  && pip3 install --upgrade -r /tmp/requirements.txt
  # && apk del build-dependencies

COPY . /app

ENV FLASK_APP=server/__init__.py
ENV TWILIO_SI="ACe343777b1ab47d98dd2c71e53a6b8030"
ENV TWILIO_AUTH="3e08fdfc79ed6fe1781664cbc6a5f2a7"
#DATABASE ENV
# ENV DATABASE="BLUDB;"
# ENV HOSTNAME="ashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;"
# ENV PORT="50000;"
# ENV PROTOCOL="TCPIP;"
# ENV UID="gqf91534;"
# ENV PWD="n8rbtmpr-0nfphqs;"
#END DATABASE ENV
CMD ["python", "manage.py", "start", "0.0.0.0:3000"]
