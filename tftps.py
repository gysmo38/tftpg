#!/usr/bin/env python
import socket, os, struct, logging, threading
from optparse import OptionParser
from tftpg_main import *
from tftps_serv import *

User = os.popen("whoami").read()

if __name__ == "__main__":
	srv = Tftp_Server()
	srv.gui.main()
	
