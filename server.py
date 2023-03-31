import time
from concurrent import futures

import google.protobuf.text_format
import grpc

import chat_pb2_grpc
import chat_pb2
import db


def create_user(login: str, full_name: str) -> chat_pb2.User:
    """Create a user."""
    user = chat_pb2.User()
    user.login = login
    user.full_name = full_name
    return user


user1 = create_user("moshhamedani", "Mosh Hamedani")
user2 = create_user("harrypotter", "Harry Potter")
users = [user1, user2]

# connect to etcd3 db
etcd = db.EtcdConnect('localhost', '2379')


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    """Operate with users and user messages."""
    def sendMessage(self, request: chat_pb2.sendMessageRequest, context) -> chat_pb2.sendMessageResponce:
        message = request.message
        message.created_at = int(time.time())
        # write data to db
        etcd.write(f'{message.to_user.login}/{message.created_at}', f'{message}')

        return chat_pb2.sendMessageResponce()  

    def getUsers(self, request: chat_pb2.getUsersRequest, context) -> chat_pb2.getMessagesResponce:
        """Returns list of users."""
        return chat_pb2.getUsersResponce(users=chat_pb2.Users(user=users))

    def getMessages(self, request: chat_pb2.getMessagesRequest, context) -> chat_pb2.getMessagesResponce:
        """Returns all messages particular user."""
        for messages in etcd.get(f'{request.user.login}'):
            for message, _ in messages:
                yield chat_pb2.getMessagesResponce(message=google.protobuf.text_format.Parse(message.decode('utf-8'), chat_pb2.Message()))


def start():
    """Run the server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port("[::]:5050")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    start()    
