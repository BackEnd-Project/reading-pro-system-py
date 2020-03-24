FROM python:3.6

WORKDIR /mnt/

ADD . .

RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r ./depoly/requirements.txt

CMD ["python3", "/mnt/run_server.py"]

EXPOSE 8080