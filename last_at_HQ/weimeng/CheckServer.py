import socket
import threading
import time


checkIP=('127.0.0.1',998)
ksocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ksocket.bind(('127.0.0.1',998))
ksocket.listen(5)
print 'wait...'



def tcplink(sock,addr):
    while True:
        k_outputs=sock.recv(2048)
        print ('1.'+str(k_outputs))
        sock.send('ok')
        #kprogres=sock.recv(1024)
        #print ('2.'+str(kprogres))
        if k_outputs=='exit' or not k_outputs:
            break

                
        
    sock.close()


while True:
    sock,addr=ksocket.accept()
    t=threading.Thread(target=tcplink(sock,addr))