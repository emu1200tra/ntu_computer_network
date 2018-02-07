import socket
import time

def ip_search(input_string):
  record = []
  flag = 0
  #print input_string
  for i in range(0 , len(input_string)-2):
    if '0' <= (input_string[i]) <= '9':
      continue
    else:
      record.append('-1')
      return record
  for i in range(0 , len(input_string)):
    for j in range(i+1 , len(input_string)-1):
      for k in range(j+1 , len(input_string)-2):
        if input_string[0:i] != '' and input_string[i:j] != '' and input_string[j:k] != '' and input_string[k:] != '':
          #print input_string[0:i] , ';' , input_string[i:j] , ';' , input_string[j:k] , ';' , input_string[k:]
          #print len(input_string[0:i]) , int(input_string[0:i]) , len(input_string[i:j]) , int(input_string[i:j]) , len(input_string[j:k]) , int(input_string[j:k]) , len(input_string[k:])-2 , int(input_string[k:])
          if 0 < len(input_string[0:i]) <= 3 and int(input_string[0:i]) <= 255 and 0 < len(input_string[i:j]) <= 3 and int(input_string[i:j]) <= 255 and 0 < len(input_string[j:k]) <= 3 and int(input_string[j:k]) <= 255 and 0 < len(input_string[k:])-2 <= 3 and int(input_string[k:]) <= 255:
            if len(str(int(input_string[0:i])) + str(int(input_string[i:j])) + str(int(input_string[j:k])) + str(int(input_string[k:]))) == len(input_string)-2:
              record.append((input_string[0:i] + '.' + input_string[i:j] + '.' + input_string[j:k] + '.' + input_string[k:]))
              flag = 1
  if flag == 0:
    record.append('-1')
    return record
  else:
    return record

f = open('config' , 'r')
place = f.read()
channel = place.split("'")
f.close()

IRCSocket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
IRCSocket.connect(('irc.freenode.net' , 6667))
IRCSocket.send(("USER jizzzz 2 3 jizzzzz\r\n")) 
IRCSocket.send("NICK ettttbotttt \r\n".encode('utf-8'))
IRCSocket.send("PRIVMSG NICKSERV :identify \r\n")

Msg = 'JOIN ' + channel[1] + '\r\n'
IRCSocket.send( Msg )
IRCSocket.send("PRIVMSG " + channel[1] + " :hi. I am robot form Mars!!\r\n")
while True:
  IRCMsg = IRCSocket.recv(4096)
  print (IRCMsg)
  if IRCMsg.find('PING') != 1:
    IRCSocket.send('PONG get the fuck up!!!\r\n')
  string = IRCMsg.split(' ')
  if len(string) > 4 and string[3] == ':@repeat':
    IRCSocket.send("PRIVMSG " + channel[1] + " :" + ' '.join(string[4:]) + "\r\n")
    time.sleep(1)
  if len(string) > 4 and string[3] == ':@convert':
    if string[4][0] == '0' and string[4][1] == 'x':
      flag = 0
      for i in range(2 , len(string[4])-2):
        if '0' <= string[4][i] <= '9' or 'a' <= string[4][i] <= 'f':
          flag = 0
        else:
          flag = 1
          break
      if flag == 0:
        IRCSocket.send("PRIVMSG " + channel[1] + " :" + str(int(''.join(string[4][2:]) , 16)) + "\r\n")
    else:
      flag = 0
      #print len(string[4])
      for i in range(0 , len(string[4])-2):
        if '0' <= string[4][i] <= '9':
          flag = 0
        else:
          flag = 1
          break
      if flag == 0:
        IRCSocket.send("PRIVMSG " + channel[1] + " :" + str(hex(int(''.join(string[4][:])))) + "\r\n")
    time.sleep(1)
  if len(string) > 4 and string[3] == ':@ip':
    return_value = ip_search(string[4])
    if return_value[0] == '-1':
      IRCSocket.send("PRIVMSG " + channel[1] + " :" + '0' + "\r\n")
    else:
      IRCSocket.send("PRIVMSG " + channel[1] + " :" + str(len(return_value)) + "\r\n")
      for i in range(0 , len(return_value)):
        IRCSocket.send("PRIVMSG " + channel[1] + " :" + return_value[i] + "\r\n")
        time.sleep(1)
    time.sleep(0.5)
  if len(string) > 3 and string[3] == ':@help\r\n':
    IRCSocket.send("PRIVMSG " + channel[1] + " :\r\n")
    IRCSocket.send("PRIVMSG " + channel[1] + " :@repeat <Message>\r\n")
    IRCSocket.send("PRIVMSG " + channel[1] + " :@convert <Number>\r\n")
    IRCSocket.send("PRIVMSG " + channel[1] + " :@ip <string>\r\n")
    time.sleep(1)