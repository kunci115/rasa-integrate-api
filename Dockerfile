FROM python:latest
COPY . /app
WORKDIR /app
COPY id_rsa.clientinstance /root/.ssh/
COPY ssh_config /root/.ssh/
RUN cat /root/.ssh/ssh_config >> /root/.ssh/config
RUN pip --default-timeout=1000 install --no-cache-dir -r requirements.txt
RUN python api.py