import random
import sys
import struct
import threading
import os
import shutil
import time
import getopt
import subprocess
import shlex

class Fuzzer:
	def __init__(self):
		self.vBoxRunning = False
		self.clientRunning = False
		self.iteration = 0
		self.pid = None
		self.UUID = "eaf256f8-9e66-4917-a8f6-14f85edacf9f"
	
	def check_env(self):
		cmd = "export LD_LIBRARY_PATH=/opt/qt56/lib"
		out = subprocess.run(cmd, shell=True)
		#print(out)

		cmd = "./VBoxManage list vms"
		args = shlex.split(cmd)
		out = subprocess.run(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)		

		try:
			rs = out.check_returncode()
			vmCount = len(out.stdout.split(b'\n'))-1
			if vmCount ==0 :
				print("vm count : ", vmCount)
				cmd = "LD_LIBRARY_PATH=/opt/qt56/lib ./VirtualBox"
				out = subprocess.run(cmd, shell=True)
				return False
			else:				
				print(out.stdout)				
		except Exception as e:
			print(e)
			return False		
		
		return True

	

	def start_xfreeRDP_2(self):
		cmd  = "xfreerdp /u:son /p:1234 /v:127.0.0.1"
		args = shlex.split(cmd)		
		proc  = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.clientRunning = True

		try:
			out = proc.communicate(timeout=4)
			print("returnCode :",  proc.returncode)		
				
		except subprocess.TimeoutExpired as e:
			print("[TimeoutExpired ] :\n", e)
			proc.kill()
			self.clientRunning = False
		except Exception as e:
			self.clientRunning = False
			proc.kill()


	def start_vBox_2(self):
		print("================ start_vBox ===============================")		
		cmd  = "./VBoxHeadless --startvm " + self.UUID + " --vrde on"
		args = shlex.split(cmd)
		proc  = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print(proc)
		print("returnCode :",  proc.returncode)		

		try:
			out = proc.communicate()
			rs = proc.poll()		
			print("proc.poll() :", rs)
			print("stdout :", out[0])
			print("stdout :", out[1])			
			print("returnCode :",  proc.returncode)

			if proc.returncode == 1:
				print("vBox is running...")
				self.vBoxRunning = True
		except Exception as e:
			print("\n[Exception ] :\n", e)
			self.vBoxRunning = False
			return

		#self.vBoxRunning = True


		


	def stop_vBox(self):		
	
		print("\n================ stop_vBox ===============================")
		cmd = "./VBoxManage controlvm " + self.UUID + " savestate"
		args = shlex.split(cmd)
		out = subprocess.run(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print("\n",out)

		try:
			rs = out.check_returncode()
		except subprocess.CalledProcessError as e: #not running
			print("\nout.returncode :" , out.returncode)
			print("[CalledProcessError ] :\n", e)		
			self.vBoxRunning = False	
			return
		#except Exception as e:
		#	print("\n[Exception ] :\n", e)
		#	return
		

		self.vBoxRunning = False #stop success


	def start(self):
		while True:
			if self.vBoxRunning == False:
				vBox_thread = threading.Thread(target=self.start_vBox_2)
				vBox_thread.setDaemon(0)
				vBox_thread.start()

			else: #vBox is running
				
				if self.clientRunning == False:
					self.start_xfreeRDP_2()

				self.iteration += 1
				

			#############################
			_counter = 1
			while _counter < 4:
				char = "*"
				time.sleep(1)
				char = char * _counter
				print(char)
				_counter += 1
				

if __name__=="__main__":
	fuzzer=Fuzzer()
	rs = fuzzer.check_env()
	if rs==True:
		fuzzer.start()


