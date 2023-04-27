from abc import ABC, abstractmethod

import etcd3 


class Db(ABC):

    """Abstract class for db."""
    
    @abstractmethod
    def write(self, key, value): pass

    @abstractmethod
    def get(self, key): pass

    @abstractmethod
    def delete(self, key): pass
        

class EtcdConnect(Db):

    """Actions with etcd db."""
    
    def __init__(self, host: str, port: str) -> None:
        """Write host and port."""
        self._host = host
        self._port = port
        self._connect()
        
    def _connect(self):
        """Connect to etcd db."""
        self._instance = etcd3.client(host=self._host, port=self._port)

    def write(self, key: str, value: str) -> None: 
        """Write data to db."""
        self._instance.put(key, value)

    def get(self, prefix: str):
        """Get data from db."""
        yield self._instance.get_prefix(prefix)
    
    def delete(self, prefix: str):
        """Delete data from db."""
        self._instance.delete_prefix(prefix)
