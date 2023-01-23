PROTO_DIR = chat_proto
PROTO_UPLOAD_TO = pb2


install:
	pip install -r requirements.txt

generate:
	git submodule update --remote
	mkdir pb2 && touch pb2/__init__.py
	echo "pb2/" >> .gitignore
	python3 -m grpc_tools.protoc -I${PROTO_DIR} --python_out=${PROTO_UPLOAD_TO} --grpc_python_out=${PROTO_UPLOAD_TO} ${PROTO_DIR}/*.proto

clean:
	rm ${PROPROTO_UPLOAD_TOTO_DIR_TO}/*_pb2.py

# Also will add the pattern for deleting pb2 folder from .gitignore after 'make clean' command
