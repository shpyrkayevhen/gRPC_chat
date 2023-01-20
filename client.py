"""Main module where implement the stuffs"""
import grpc

from chat_proto import chat_pb2_grpc, chat_pb2


def create_message():
    message = chat_pb2.Message()
    message.id = 1
    message.from_user.login = "moshhamedani"
    message.to_user.login = "mirabuchkovska"
    # message.created_at specify on the server side
    message.body = "Hi, Mira! Can you call me back today. Second message?"
    return message


def create_user():
    user = chat_pb2.User()
    user.login = "mirabuchkovska"
    user.fullName = "Mosh Hamedani"
    return user


def run():
    
    with grpc.insecure_channel("0.0.0.0:5050") as channel:
        
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        while True:
            
            grpc_call = input(
                "What would like to do? chat_pb2.Message \n \
                '1' - SEND MESSAGE \n \
                '2' - GET USERS \n \
                '3' - GET ALL USER MESSAGES \n \
                '4' - EXIT \n \
                Please enter the number: "
            ).strip()
            
            match grpc_call:

                case "1":
                    # Make the call to server for sending a message
                    response = stub.sendMessage(chat_pb2.sendMessageRequest(message=create_message()))
        
                case "2":
                    # Make the call to server for getting the users
                    listOfUsers = stub.getUsers(chat_pb2.getUsersRequest())
                    print(listOfUsers)     

                case "3":
                    # Create the user and get all his messages from server
                    for message in stub.getMessages(chat_pb2.getMessagesRequest(user=create_user())):
                        print(message)

                case "4":
                    break
        

if __name__ == "__main__":
    run()
