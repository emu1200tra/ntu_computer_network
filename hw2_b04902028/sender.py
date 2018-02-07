import socket
import time

packet_size = 1024
time_out = 1

def input_arg():
  ip = raw_input("input ip of agent:")
  port = input("input port of agent:")
  ip_des = raw_input("input ip of receiver:")
  port_des = input("input port of receiver:")
  ip_self = raw_input("input ip of sender:")
  port_self = input("input port of sender:")
  sorce_file = raw_input("input sorce file path:")
  threshold = input("input threshold:")
  print "done input"
  return ip , port , ip_des , port_des , ip_self , port_self , sorce_file , threshold


def build_socket(ip , port):
  AgentSocket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
  RecvSocket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
  RecvSocket.bind((ip , port))
  return AgentSocket , RecvSocket


def connect_socket(socket_name):
  socket_name.settimeout(time_out)
  return socket_name


def read_in_file(sorce_file):
  f = open(sorce_file , 'rb')
  data = f.read()
  f.close()
  return data


def segment_data(data):
  flag = len(data) % packet_size
  Npart = 0
  data_list = []
  Npart = int(len(data) / packet_size)
  for i in range(Npart):
    data_list.append(str(i) + '\n' + data[i*packet_size : (i+1)*packet_size])
  if flag != 0:
    data_list.append(str(Npart) + '\n' + data[Npart*packet_size:])
  if len(data) == 0:
    data_list.append(str(0) + '\n' + '')
  return data_list


def increase_window(window , threshold):
  if int(window) < int(threshold):
    return int(window) * 2
  else:
    return int(window) + 1


def reset_threshold(window):
  window = int(window)
  print "window:" , window
  return max(int(window/2) , 1)

def check_send_and_receive(send , receive):
  counter = 0
  resend = []
  for i in range(len(send)):
    if i < len(receive) and int(receive[i]) == int(send[i]):
      counter +=1
    elif i < len(receive) and int(receive[i]) != int(send[i]):
      resend.append(send[i])
    else:
      resend.append(send[i])
  return counter , resend


if __name__ == '__main__':

  #init
  ip , port , ip_des , port_des , ip_self , port_self , sorce_file , threshold = input_arg()
  data = read_in_file(sorce_file)
  data_list = segment_data(data)
  subfile = sorce_file.split(".")
  print "subfile:" , subfile
  window = 1
  window_start = 0
  AgentSocket , RecvSocket = build_socket(ip_self , port_self)
  #start sending
  print "done setting....start sending"
  counter = 0
  if len(subfile) == 2:
    subfile = subfile[1]    
  else:
    subfile = "NoSubfile"
  resend = []
  last_ack = 0
  while last_ack != (len(data_list)-1):
    #send file in window
    send = []
    for j in range(int(window)):
      #avoid out of window
      window_start = int(window_start)
      if int(window_start) + j < len(data_list):
        AgentSocket = connect_socket(AgentSocket)
        AgentSocket.sendto( str(ip_des) + "\n" + str(port_des) + "\n" + str(subfile) + "\n" + str(ip_self) + "\n" + str(port_self) + "\n" + str(data_list[window_start+j]) , (ip , port))
        send.append(int(window_start) + j)
        if not((int(window_start) + j) in resend):
          print "send data: #" , str(int(window_start)+j) , "with window size = " + str(window)
        else:
          print "resend data: #" , str(int(window_start)+j) , "with window size = " + str(window)    
    #done sending window
    #start receive ack
    receive = []
    record_ack = -1
    while record_ack != send[-1]:
      RecvSocket = connect_socket(RecvSocket)
      #receive ack with timeout
      try:
        ack = RecvSocket.recvfrom(1024)
        ack = ack[0].split("\n")
        ack = ack[2]
        ack = ack.split('#')
        ack = ack[1]
        window_start = int(ack)+1
        receive.append(ack)
        record_ack = int(ack)
        print "receive ack: #" , str(ack)
        last_ack = record_ack
      #if timeout
      except socket.timeout:
        threshold = reset_threshold(window)
        window = 1
        print "timeout!! threshold = " , str(threshold)
        break
    #change counter and window
    flag , resend = check_send_and_receive(send , receive)
    if flag == len(send):
      window = increase_window(window , threshold)
    counter += flag
  #send fin
  AgentSocket = connect_socket(AgentSocket)
  AgentSocket.sendto(str(ip_des) + '\n' + str(port_des) + '\n' + "fin" + "\n" + str(ip_self) + "\n" + str(port_self) + '\n' + "fin", (ip , port))
  print "send fin"
  #receive finack
  while True:
    try:
      finack = RecvSocket.recvfrom(1024)
      print "receive finack"
      break
    #timeout , resend
    except socket.timeout:
      print "resend fin for time out"
      AgentSocket = connect_socket(AgentSocket)
      AgentSocket.sendto(str(ip_des) + '\n' + str(port_des) + '\n' + "fin" + "\n" + str(ip_self) + "\n" + str(port_self) + '\n' + "fin" , (ip , port))

  print "done sending file"

    
