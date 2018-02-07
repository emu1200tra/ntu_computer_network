import socket

def parameter_input():
  buffer_size = input("buffer_size:")
  file_name = raw_input("filename(no extended filename):")
  ip_self = raw_input("self ip:")
  port_self = input("self port:")
  ip_agent = raw_input("agent ip:")
  port_agent = input("agent port:")
  return buffer_size , file_name , ip_self , port_self , ip_agent , port_agent

def build_socket(ip_self , port_self):
  AgentSocket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
  RecvSocket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
  RecvSocket.bind((ip_self , port_self))
  return AgentSocket , RecvSocket

def open_file(file_name , subfilename):
  if subfilename == "":
    f = open(file_name , 'wb')  
  else:
    f = open(file_name + '.' + subfilename , 'wb')
  return f

def write_data(data , file_object):
  for i in range(len(data)):
    write_data = data[i].split("\n")  
    write_data = write_data[6:]
    write_data = '\n'.join(write_data)
    file_object.write(write_data)


if __name__ == '__main__':

  buffer_size , file_name , ip_self , port_self , ip_agent , port_agent = parameter_input()
  AgentSocket , RecvSocket = build_socket(ip_self , port_self)
  file_object = 0
  in_buffer = 0
  previous_packet_num = -1
  get_subfile = 0
  data = []
  while True:
    #receive data
    receive_packet = RecvSocket.recvfrom(4096)
    #print "check:" , receive_packet[0]
    packet = receive_packet[0].split('\n')
    #if fin
    if packet[2] == "fin":
      print "receive fin"
      #if packet in buffer, flush
      if in_buffer != 0:
        print "still have packet in buffer. flush."
        write_data(data , file_object)
      print "send finack"
      AgentSocket.sendto(packet[3] + "\n" + packet[4] + "\n#finack" , (ip_agent , port_agent))
      print "close connection"
      break
    print "receive data:" , packet[5]
    #if loss packet during sending
    if int(previous_packet_num) + 1 != int(packet[5]):
      print "drop data:" , packet[5] , "for error seq_num"
      AgentSocket.sendto(packet[3] + "\n" + packet[4] + "\n#" + str(previous_packet_num) , (ip_agent , port_agent))
      print "send ack:" , previous_packet_num
    #if buffer is full
    elif in_buffer == buffer_size:
      print "drop data:" , packet[5] , "for full buffer"
      AgentSocket.sendto(packet[3] + "\n" + packet[4] + "\n#" + str(previous_packet_num) , (ip_agent , port_agent))
      print "send ack:" , previous_packet_num
      print "flush data"
      write_data(data , file_object)
      in_buffer = 0
      data = []
    #get correct data and put in buffer
    else:
      in_buffer += 1
      data.append(receive_packet[0])
      previous_packet_num = int(packet[5])
      #get subfilename
      if get_subfile == 0:
        if packet[2] == "NoSubfile":
          subfilename = ''
          file_object = open_file(file_name , subfilename)
          get_subfile = 1
        else:
          subfilename = packet[2]
          get_subfile = 1
          file_object = open_file(file_name , subfilename)
      #send ack
      AgentSocket.sendto(packet[3] + "\n" + packet[4] + "\n#" + str(previous_packet_num) , (ip_agent , port_agent))
      print "send ack:" , previous_packet_num

