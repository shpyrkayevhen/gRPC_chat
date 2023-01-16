import chat_pb2_grpc
import chat_pb2
import grpc
import time

from concurrent import futures


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
    

# Create server. Connect ip and port for listening
if __name__ == "__main__":
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)

    print("Server Started")

    server.add_insecure_port("[::]:5050")
    server.start()
    try:
        server.wait_for_termination()
    except:
        del ChatServiceServicer.users
        print("Server end")


    