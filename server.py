from concurrent import futures
import time

import grpc

from chat_proto import chat_pb2_grpc, chat_pb2


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    

    list_of_users = chat_pb2.Users()

    list_of_messages = []


    def sendMessage(self, request, context):

        message = request.message
        message.created_at = time.time()
        ChatServiceServicer.list_of_messages.append(message)

        # Check users if they exist in our system
        if message.from_user not in ChatServiceServicer.list_of_users.user:
            ChatServiceServicer.list_of_users.user.add(login=message.from_user.login)

        if message.to_user not in ChatServiceServicer.list_of_users.user:
            ChatServiceServicer.list_of_users.user.add(login=message.to_user.login)


        return chat_pb2.sendMessageResponce()
    

    def getUsers(self, request, context):
            
        return chat_pb2.getUsersResponce(users=ChatServiceServicer.list_of_users)
    

    def getMessages(self, request, context):
        
        user_login = request.user.login

        for message in ChatServiceServicer.list_of_messages:
            if message.from_user.login == user_login:
                yield chat_pb2.getMessagesResponce(message=message)
                time.sleep(3)


if __name__ == "__main__":
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port("[::]:5050")
    server.start()
    server.wait_for_termination()
    