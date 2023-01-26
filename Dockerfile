FROM python
WORKDIR /usr/src/grpc-chat
COPY requirements.txt ./
COPY Makefile ./
RUN make install 
EXPOSE 5050
COPY . .
RUN make generate
CMD [ "python", "server.py" ]
