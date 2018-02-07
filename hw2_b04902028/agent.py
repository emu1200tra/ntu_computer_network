import socket
import random

def input_parameter():
  ip = raw_input("ip:")
  port = input("port:")
  loss_rate = input("loss rate:")
  return ip , port , loss_rate

def build_socket(ip , port):
  udpsocket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
  udpsocket.bind((ip , port))
  sendersocket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
  return udpsocket , sendersocket

def drop_or_not(loss_rate):
  base = loss_rate * 1000.0
  div = random.randint(1 , 1000)
  if div <= base:
    return 1
  else:
    return 0

if __name__ == "__main__":
  ip , port , loss_rate = input_parameter()
  udpsocket , sendersocket = build_socket(ip , port)
  #done process init, start get linking
  print "wait for first link..."
  total_packet = 0.0
  count_loss_rate = 0.0
  while True:
    print "get connection"
    packet = udpsocket.recvfrom(4096)
    data = packet[0].split('\n')
    if data[2][0] == '#':
      #if receive ack, don't drop
      print "get ack:" , data[2][1:]
      sendersocket.sendto(packet[0] , (data[0] , int(data[1])))
      print "fwd ack:" , data[2][1:]
      if data[2][1:] == "finack":
        total_packet = 0.0
        count_loss_rate = 0.0
    else:
      print "get data:" , data[5]
      total_packet += 1
      #drop or not
      flag = drop_or_not(loss_rate)
      #drop
      if flag:
        count_loss_rate += 1
        print "drop data:" , data[5] , "with drop rate:" , float(count_loss_rate / total_packet)
      else:
        print "fwd data:" , data[5]
        sendersocket.sendto(packet[0] , (data[0] , int(data[1])))
    




   