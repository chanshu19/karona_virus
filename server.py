import socket                
import sys

# next create a socket object 
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)          
            
# Next bind to the port 
s.bind(('192.168.0.104', 5001))         
# put the socket into listening mode 
s.listen(3)      
print ("socket is listening at port : ",5001)            
  
#accept the connection
c, addr = s.accept()      
print ('Got connection from', addr) 
client_response = str(c.recv(2048),'utf-8')
print(client_response,end="")

while True: 
   cmd = input(" : ")
   if cmd == 'quit':
      c.close()
      s.close()
      sys.exit()

   elif len(str.encode(cmd))>0:      
      try:
         c.send(str.encode(cmd))
         client_response = str(c.recv(2048),'utf-8')
         print(client_response,end="")
      except Exception as e:
         print('error by server',e)
c.close()

