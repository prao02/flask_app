FROM alpine

RUN apk add --no-cache python3-dev && apk add cmd:pip3

WORKDIR /app_flask

COPY /requirement.txt /app_flask

RUN pip3 install -r requirement.txt

COPY ["test.py", "/app_flask"]

EXPOSE 5002

ENTRYPOINT ["python3"]

CMD ["test.py"]
