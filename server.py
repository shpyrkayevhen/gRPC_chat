from concurrent import futures
import time

import grpc

from chat_proto import chat_pb2_grpc, chat_pb2


def run():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port("[::]:5050")
    server.start()
    server.wait_for_termination()


users = chat_pb2.Users()
messages = {}


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
        
    def sendMessage(self, request, context):
        message = request.message
        message.created_at = time.time()
             
        if message.to_user.login not in messages:
            messages[message.to_user.login] = list()
            messages[message.to_user.login].append(message)
        else:
            messages[message.to_user.login].append(message)

        # Check if users exist in our system
        if message.from_user not in users.user:
            users.user.add(login=message.from_user.login)

        if message.to_user not in users.user:
            users.user.add(login=message.to_user.login)

        return chat_pb2.sendMessageResponce()  

    def getUsers(self, request, context):
        return chat_pb2.getUsersResponce(users=users)

    def getMessages(self, request, context):
        user_login = request.user.login
        if user_login in messages:
            for message in messages[user_login]:
                yield chat_pb2.getMessagesResponce(message=message)


if __name__ == "__main__":
    run()    
