PROTO_DIR =.

generate:
	python3 -m grpc_tools.protoc -I${PROTO_DIR} --python_out=${PROTO_DIR} --grpc_python_out=${PROTO_DIR} ${PROTO_DIR}/*.proto

clean:
	rm ${PROTO_DIR}/*_pb2.py


# 1: make generate 
# 2: make clean