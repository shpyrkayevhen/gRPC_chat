PROTO_DIR = chat_proto


install:
	pip install -r requirements.txt

generate:
	python3 -m grpc_tools.protoc -I${PROTO_DIR} --python_out=${PROTO_DIR} --grpc_python_out=${PROTO_DIR} ${PROTO_DIR}/*.proto

clean:
	rm ${PROTO_DIR}/*_pb2.py

