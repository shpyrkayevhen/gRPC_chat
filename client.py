from pprint import pprint
import chat_pb2_grpc
import chat_pb2
import grpc


def sendMessage():

    message = chat_pb2.Message()
    message.id = 1
    message.from_user.login = "moshhamedani"
    message.to_user.login = "mirabuchkovska"
    # message.created_at specify on the server side
    message.body = "Hi, Yevhen! Can you call me back today?"

    return message


def run():

    with grpc.insecure_channel("0.0.0.0:5050") as channel:
        
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # Make the calls to server
        response = stub.sendMessage(chat_pb2.sendMessageRequest(message=sendMessage()))
        print(response)

        listOfUsers = stub.getUsers(chat_pb2.getUsersRequest())
        print(listOfUsers)


if __name__ == "__main__":
    run()
    





















