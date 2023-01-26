FROM python
WORKDIR /usr/src/grpc_chat
COPY requirements.txt ./
COPY Makefile ./
RUN make install
RUN make generate 
EXPOSE 5050
COPY . .
CMD [ "python", "server.py" ]