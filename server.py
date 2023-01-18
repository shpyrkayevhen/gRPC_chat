import chat_proto.chat_pb2_grpc as chat_pb2_grpc
import chat_proto.chat_pb2 as chat_pb2
from concurrent import futures
import grpc
import time


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    

    # List of users
    users = chat_pb2.Users()
    
    # List of messages
    messages = []


    def sendMessage(self, request, context):

        message = request.message
        message.created_at = time.time()
        ChatServiceServicer.messages.append(message)

        # Check users if they exist in our system
        if message.from_user not in ChatServiceServicer.users.user:
            ChatServiceServicer.users.user.add(login=message.from_user.login)

        if message.to_user not in ChatServiceServicer.users.user:
            ChatServiceServicer.users.user.add(login=message.to_user.login)


        return chat_pb2.sendMessageResponce()
    

    def getUsers(self, request, context):
            
        return chat_pb2.getUsersResponce(users=ChatServiceServicer.users)
    

    def getMessages(self, request, context):
        
        user_login = request.user.login

        for message in ChatServiceServicer.messages:
            if message.from_user.login == user_login:
                yield chat_pb2.getMessagesResponce(message=message)
                time.sleep(3)



if __name__ == "__main__":
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)

    print("Server Started")

    server.add_insecure_port("[::]:5050")
    server.start()
    
    try:
        server.wait_for_termination()
    except:
        print("Server end")


    