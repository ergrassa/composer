FROM python:3.10-slim
WORKDIR /app
COPY ./ .
EXPOSE 80
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "-u", "main.py" ]
