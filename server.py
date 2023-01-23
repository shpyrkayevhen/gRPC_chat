import time
from concurrent import futures

import grpc

from pb2 import chat_pb2, chat_pb2_grpc


def create_user(login, full_name):
    """Create a user."""
    user = chat_pb2.User()
    user.login = login
    user.fullName = full_name
    return user


user1 = create_user("moshhamedani", "Mosh Hamedani")
user2 = create_user("harrypotter", "Harry Potter")


messages = {}
users = [user1, user2]
message_id = 1


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    """Operate with users and user messages."""
    def sendMessage(self, request, context):
        global message_id
        message = request.message
        message.id = message_id
        message_id += 1 
        message.created_at = time.time()
             
        if message.to_user.login not in messages:
            messages[message.to_user.login] = list()
            messages[message.to_user.login].append(message)
        else:
            messages[message.to_user.login].append(message)

        return chat_pb2.sendMessageResponce()  

    def getUsers(self, request, context):
        """Returns list of users."""
        return chat_pb2.getUsersResponce(users=chat_pb2.Users(user=users))

    def getMessages(self, request, context):
        """Returns all messages particular user."""
        user_login = request.user.login
        if user_login in messages:
            for message in messages[user_login]:
                yield chat_pb2.getMessagesResponce(message=message)


def start():
    """Run the server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port("[::]:5050")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    start()    
