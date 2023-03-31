from abc import ABC, abstractmethod

import etcd3 


class Db(ABC):
    '''Abstract class for db.'''
    @abstractmethod
    def write(self, key=None, value=None): pass

    @abstractmethod
    def get(self, key): pass

    @abstractmethod
    def delete(self, key): pass
        

class EtcdConnect(Db):
    '''Actions with etcd db.'''
    def __init__(self, host: str, port: str) -> None:
        '''Write host and port.'''
        self._host = host
        self._port = port

    def _connect(self):
        '''Connect to etcd db.'''
        self._instance = etcd3.client(host=self._host, port=self._port)

    def write(self, key: str, value) -> None: 
        '''Write data to db.'''
        self._connect()
        self._instance.put(key, value)
        self._instance.close()

    def get(self, prefix: str):
        '''Get data from db.'''
        self._connect()    
        yield self._instance.get_prefix(prefix)
        self._instance.close()
    
    def delete(self, prefix: str):
        '''Delete data from db.'''
        self._connect()  
        self._instance.delete_prefix(prefix)
        self._instance.close()
