FROM python:3.11.1
WORKDIR /usr/src/grpc-chat
COPY requirements.txt .
COPY Makefile .
RUN make install
EXPOSE 5050
COPY . .
RUN make generate
CMD [ "python", "server.py" ]
