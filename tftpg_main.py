import pygtk
pygtk.require('2.0')
import gtk
import gobject


class Tftp_Server_GUI:
	""" fenetre principale de tftps """
	def __init__(self,srv):
		
		#Thread
		gobject.threads_init()
		
		self.srv = srv	
		# Conf of main win
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("TftpS")
		self.window.set_default_size(500,400)
		
		self.box_main = gtk.VBox(False)
				
		#Top win
		self.fra_conf = gtk.Frame("Configuration")
		self.box_conf_main = gtk.VBox()
		
		#1st row 
		self.box_conf_row1 = gtk.HBox()
		self.lab_dir = gtk.Label("Current directory: ")
		self.com_file = gtk.combo_box_new_text()
		self.but_bro = gtk.Button("Browse ")
		self.box_conf_row1.pack_start(self.lab_dir)
		self.box_conf_row1.pack_start(self.com_file)
		self.box_conf_row1.pack_start(self.but_bro)
		self.box_conf_main.pack_start(self.box_conf_row1)
		
		#2nd row
		self.box_conf_row2 = gtk.HBox()
		self.lab_srv_int = gtk.Label("Listen interface: ")
		self.com_srv_ip = gtk.combo_box_new_text()
		self.but_dir = gtk.Button("Show dir ")
		self.box_conf_row2.pack_start(self.lab_srv_int)
		self.box_conf_row2.pack_start(self.com_srv_ip)
		self.box_conf_row2.pack_start(self.but_dir)
		self.box_conf_main.pack_start(self.box_conf_row2)
		
		self.fra_conf.add(self.box_conf_main)
		self.box_main.pack_start(self.fra_conf,False,False)
		
		#Middle win
		self.fra_srv = gtk.Frame("Serveur activities")
		self.tvi_srv = gtk.TextView()
		self.tvi_srv.set_editable(False)
		
		self.fra_srv.add(self.tvi_srv)
		
		self.box_main.pack_start(self.fra_srv)
		
		#Bottom win
		self.box_bottom = gtk.HBox()
		self.but_about = gtk.Button(stock=gtk.STOCK_ABOUT)
		self.but_sett = gtk.Button("Settings")
		self.but_help = gtk.Button(stock=gtk.STOCK_HELP)
		self.but_quit = gtk.Button(stock=gtk.STOCK_QUIT)
		self.but_quit.connect("clicked",self.quit,None)
		self.box_bottom.pack_start(self.but_about)
		self.box_bottom.pack_start(self.but_sett)
		self.box_bottom.pack_start(self.but_help)
		self.box_bottom.pack_start(self.but_quit)
		
		self.box_main.pack_start(self.box_bottom,False,False)
		
		self.window.add(self.box_main)
		self.window.connect("delete_event",self.delete_event)
		self.window.connect("destroy",self.quit)
		self.window.show_all()
	
	
	def main(self):
		gtk.main()

	def delete_event(self, widget, event, data=None):
		return False
	
	def quit(self,widget,data=None):
		print "Thanks using TftpS :) Bye..."
		self.srv.Thread_Clt._Thread__stop()
		gtk.main_quit()
