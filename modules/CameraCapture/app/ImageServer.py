import socket
import sys
import threading
import time
import base64

class ImageServerConnection():
    def __init__(self, ipAddr, connection):
        self.connection = connection
        self.ip = ipAddr
        self.data = []

    def recv(self):
        self.data = []
        while True:
            temp = self.connection.recv(2048)
            if temp :
                self.data.append(temp)
            else:
                break
        return self.data
    
    def send(self, payload):
        try:
            self.connection.sendall(payload)
        except Exception as e:
            print('ImageServerConnection(' + str(self.ip) + ')::Excpetion on Send -' + str(e))
    
    def close(self):
        self.connection.close()
        print ('ImageServerConnection(' + str(self.ip) + ')::Closed.')

class ImageServer(threading.Thread):
    def __init__(self, ipAddr, port):
        threading.Thread.__init__(self)
        self.ipAddr = ipAddr
        self.port = port
        self.socket = None
        self.clients = []

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('ImageServer::Socket created.')

        self.socket.bind((self.ipAddr, self.port))
        print('ImageServer::Socket bind complete.')

        self.socket.listen(10)
        print('ImageServer::Socket now listening.')

        try:
            while True :
                conn, ipAddr = self.socket.accept()
                client = ImageServerConnection(ipAddr, conn)
                self.clients.append(client)
                print ('ImageServer::client connected - ' + str(client.ip))
                self.recv_from_clients()
        except:
            print('ImageServer::exited run loop.')

    def recv_from_clients(self):
        for client in self.clients :
            data = client.recv()
            if data:
                print ('ImageServer::data received from ' + str(client.ip))
                print (str(data))

    def broadcast(self, frame):
        try:
            if len(self.clients) > 0:
                print ('ImageServer::brocasting...')
                b64 = base64.encodestring(frame)
                payload = "<html><img src='data:image/png;base64,"+ b64 +"'></html>"
                print(payload)
                for client in self.clients :
                    client.send(payload)
                print ('ImageServer::brocasting completed.')
        except Exception as e:
            print('ImageServer::Exception on broadcast -' + str(e))

    def close(self):
        print ('ImageServer::Closing...')
        for client in self.clients:
            client.close()
        self.socket.close()
        print ('ImageServer::Closed.')