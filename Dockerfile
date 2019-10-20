FROM python:latest
COPY . /app
WORKDIR /app
COPY id_rsa.clientinstance /root/.ssh/
COPY id_rsa.pub /root/.ssh/
COPY ssh_config /root/.ssh/config
RUN chmod 600 /root/.ssh/id_rsa.clientinstance
RUN pip --default-timeout=1000 install --no-cache-dir -r requirements.txt
RUN python api.py