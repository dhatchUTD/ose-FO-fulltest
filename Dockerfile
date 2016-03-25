FROM python:2.7.11
MAINTAINER David Hatch "david.hatch@wolterskluwer.com"

RUN apt-get update && apt-get install -y \
unzip \
libaio-dev

COPY . /tmp

RUN mkdir /opt/server && \
mv /tmp/server/* /opt/server && \
mkdir /opt/oracle && \
unzip /tmp/oracle/basiclite-11.1.0.7.0-linux-x86_64.zip -d /opt/oracle && \
unzip /tmp/oracle/sdk-11.1.0.7.0-linux-x86_64.zip -d /opt/oracle && \
ln -s /opt/oracle/instantclient_11_1/libclntsh.so.11.1 /opt/oracle/instantclient_11_1/libclntsh.so

#RUN chcon -R -t textrel_shlib_t /opt/oracle/instantclient_11_1

ENV LD_RUN_PATH=/opt/oracle/instantclient_11_1 ORACLE_HOME=/opt/oracle/instantclient_11_1 

RUN pip install cx_Oracle && pip install -r /tmp/requirements.txt && rm -r /tmp/*

WORKDIR /opt/server

EXPOSE 8086
CMD ["python", "rest_server.py"]
