from tftpg_main import *
from tftps import *

class Tftp_Server():
	
	def __init__(self):
		self.Server_ip = "127.0.0.1"
		self.Server_port = 1069
		self.Server_socket_udp = None
		self.Server_dir = "/home/foel8361/tftp/"
		self.gui = Tftp_Server_GUI(self)
		self.Server_set_dir()
		self.Server_set_int()
		self.Server_start()
		
	def Server_start(self):
			self.Server_write_msg("(TODO DATE) - Starting server...\n")
			try:
				self.Server_socket_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
				self.Server_socket_udp.bind((self.Server_ip,self.Server_port))
			except socket.error:
				print("Problem with socket. Check if you are root or admin")
				exit();
			
			self.Server_write_msg("(TODO DATE) - Serveur ready to fly....\n")	
			#~ self.Server_recv_data()
			self.Thread_Clt = Thread_Client(self)
			self.Thread_Clt.start()
	
	def Server_set_dir(self):
		self.gui.com_file.append_text(self.Server_dir)
		self.gui.com_file.set_active(0)
	
	def Server_write_msg(self,msg):
		buf_ban = self.gui.tvi_srv.get_buffer()	
		ban = (msg)
		buf_ban.insert_at_cursor(ban)
		self.gui.tvi_srv.set_buffer(buf_ban)
	
	def Server_set_int(self):
		self.gui.com_srv_ip.append_text("%s" % (self.Server_ip))
		self.gui.com_srv_ip.set_active(0)

	
	def Server_debug(debug_text):
			print "DEBUG: ",debug_text

class Thread_Client(threading.Thread):
	"""Thread class for reception packets"""
	def __init__(self,srv):
		threading.Thread.__init__(self)
		self.Server_blck_size = 516
		# A table about the client
		# [0] -> @IP
		# [1] -> Filename
		# [2] -> Mode
		# [3] -> Seq_num
		# [4] -> Packet size
		# [5] -> Data
		# [6] -> Num packets to send
		# [7] -> Pos in send file
		self.Client_infos = ['none']*8
		self.Client_seppos = []
		self.Client_opcode = None
		self.Client_num_sepbyte = 0
		self.srv = srv

		self.Client_data = []
		self.Client_file_receive = ""
		self.Client_file_sending = ""
		
	def run(self):
		name = self.getName()
		self.srv.Server_write_msg("(TODO DATE) - Waiting for client  %s...\n" % name)

		while 1:			
			self.Client_data, self.Client_infos[0] = self.srv.Server_socket_udp.recvfrom(self.Server_blck_size)
			(self.Client_opcode,) = struct.unpack("!H", self.Client_data[:2])
			length = 0
			for byte in self.Client_data:
				if ord(byte) == 0:
					self.Client_seppos.append(length)
				length += 1
			#RRQ Packet
			if self.Client_opcode == 1:
				self.srv.Server_write_msg("(TODO DATE) - Receive RRQ packet\n")
				self.Rcv_RRQ_packet()
				self.Open_file()
				self.Send_DATA_packet()
					
			#WRQ Packet
			elif self.Client_opcode == 2:
				self.Rcv_WRQ_packet()	
				self.Send_ACK(0)
			#DATA Packet
			elif self.Client_opcode == 3:
				#self.srv.Server_write_msg(".")	
				self.Rcv_DATA_packet()
				self.Send_ACK(self.Client_infos[3])
		#		self.srv.Server_write_msg("#")
				if self.Client_infos[4] < 516:
					self.srv.Server_write_msg("#\n")
					self.srv.Server_write_msg("(TODO DATE) - Finished receiving the file\n")
					self.Write_file()
					self.Client_infos = ['none']*6
			#ACK Packet
			elif Client_opcode == 4:
				self.srv.Server_write_msg("(TODO DATE) - Receive ACK packet\n")
			#Error Packet
			elif Client_opcode == 5:
				self.srv.Server_write_msg("(TODO DATE) - Receive ERROR packet\n")
			#Kesako? Unknown packet :p
			else :
				self.srv.Server_write_msg("(TODO DATE) - Receive UNKNOWN packet\n")
				

	def Send_ACK(self,num_ack):
		self.Packet_ACK = struct.pack("!HH", 4, num_ack)
		self.srv.Server_socket_udp.sendto(self.Packet_ACK,self.Client_infos[0])
		
	def Rcv_WRQ_packet(self):
		self.Client_infos[1] = self.Client_data[2:self.Client_seppos[1]]
		self.Client_infos[2] = self.Client_data[self.Client_seppos[1]:self.Client_seppos[2]]	
		self.srv.Server_write_msg("(TODO DATE) - Starting receive %s from %s...\n" % (self.Client_infos[1], self.Client_infos[0]))		

	def Rcv_RRQ_packet(self):
		self.Client_infos[1] = self.Client_data[2:self.Client_seppos[1]]
		self.Client_infos[2] = self.Client_data[self.Client_seppos[1]:self.Client_seppos[2]]	
		self.srv.Server_write_msg("(TODO DATE) - Starting sending %s from %s...\n" % (self.Client_infos[1], self.Client_infos[0]))		
		
	def Rcv_DATA_packet(self):
	#	Server_debug("Receive DATA packet num %s" % Client_infos[3])
		self.Client_infos[4] = len(self.Client_data)
		(self.Client_infos[3],) = struct.unpack("!H", self.Client_data[2:4])
		self.Client_infos[5] += self.Client_data[4:]
	#	print "."
	
	def Send_DATA_packet(self):
		self.srv.Server_write_msg("SEND DATA Packet")
	 
	def Write_file(self):
		full_filename = self.srv.Server_dir + self.Client_infos[1]
		self.Server_receive_file = open(full_filename,'w')
		self.Server_receive_file.write(self.Client_infos[5])
		self.Server_receive_file.close()
	#	print "Download of",self.Client_infos[1],"from",self.Client_infos[0],"finished"			

	def Open_file(self):
		full_filename = self.srv.Server_dir + self.Client_infos[1]
		self.Server_file_sending = open(full_filename,'r')
		self.Server_file_sending.close()

