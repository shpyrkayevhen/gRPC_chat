import protos.chat_pb2_grpc as chat_pb2_grpc
import protos.chat_pb2 as chat_pb2
import grpc


def message():

    message = chat_pb2.Message()
    message.id = 1
    message.from_user.login = "moshhamedani"
    message.to_user.login = "mirabuchkovska"
    # message.created_at specify on the server side
    message.body = "Hi, Mira! Can you call me back today?"

    return message


def run():
   
    with grpc.insecure_channel("0.0.0.0:5050") as channel:
        
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # Make the call to server for sending a message
        response = stub.sendMessage(chat_pb2.sendMessageRequest(message=message()))
    
        # Make the call to server for getting the users
        listOfUsers = stub.getUsers(chat_pb2.getUsersRequest())
        print(listOfUsers)

if __name__ == "__main__":
    run()




















