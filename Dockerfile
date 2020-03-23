FROM dootech/python:3.6-slim-dep
WORKDIR /mnt/
ADD . .
# RUN start.sh
CMD ["python3", "/mnt/run_server.py"]
# EXPOSE 8080
EXPOSE 8080