PROTO_DIR = chat_proto


install:
	pip install -r requirements.txt

generate:
	git submodule update --init
	python3 -m grpc_tools.protoc -I${PROTO_DIR} --python_out=. --grpc_python_out=. ${PROTO_DIR}/*.proto

clean:
	rm *_pb2.py
