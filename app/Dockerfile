FROM python:3.7
COPY . /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]