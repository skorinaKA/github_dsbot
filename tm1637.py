'''
python-periphery TM1637 4Digits 8Segment LCD example

I ported from here
https://github.com/johnlr/raspberrypi-tm1637

'''
#!/usr/bin/python
#-*- encoding: utf-8 -*-

import discord
from discord.ext import commands
import publicip
import requests
import json
import re
import time
import subprocess
from time import time, sleep, localtime
from periphery import GPIO
from io import StringIO
from contextlib import redirect_stdout

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

#client = discord.Client(intentss=discord.Intents.all())
#client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

CLK = 2 # GPIO for CLK
DIO = 3 # GPIO for DIO

gpio_clk = GPIO(CLK, "out")
gpio_dio = GPIO(DIO, "out")


"""
	  A
	 ---
  F |	| B
	 -G-
  E |	| C
	 ---
	  D

"""


class TM1637:
	I2C_COMM1 = 0x40
	I2C_COMM2 = 0xC0
	I2C_COMM3 = 0x80
	digit_to_segment = [
		0b0111111, # 0
		0b0000110, # 1
		0b1011011, # 2
		0b1001111, # 3
		0b1100110, # 4
		0b1101101, # 5
		0b1111101, # 6
		0b0000111, # 7
		0b1111111, # 8
		0b1101111, # 9
		0b1110111, # A
		0b1111100, # b
		0b0111001, # C
		0b1011110, # d
		0b1111001, # E
		0b1110001, # F
		0b1000000  # -
		]

	def __init__(self, clk, dio):
		self.clk = clk
		self.dio = dio
		self.brightness = 0x0f

		self.gpio_clk = GPIO(self.clk, "out")
		self.gpio_dio = GPIO(self.dio, "out")

	def bit_delay(self):
		sleep(0.001)
		return
   
	def set_segments(self, segments, pos=0):
		# Write COMM1
		self.start()
		self.write_byte(self.I2C_COMM1)
		self.stop()

		# Write COMM2 + first digit address
		self.start()
		self.write_byte(self.I2C_COMM2 + pos)

		for seg in segments:
			self.write_byte(seg)
		self.stop()

		# Write COMM3 + brightness
		self.start()
		self.write_byte(self.I2C_COMM3 + self.brightness)
		self.stop()

	def start(self):
		self.gpio_clk.write(True)
		self.gpio_dio.write(True)
		self.gpio_dio.write(False)
		self.gpio_clk.write(False)
   
	def stop(self):
		self.gpio_clk.write(False)
		self.gpio_dio.write(False)
		self.gpio_clk.write(True)
		self.gpio_dio.write(True)
  
	def write_byte(self, data):
		#print("data={:x}".format(data))
		for i in range(8):
			self.gpio_clk.write(False)
			if data & 0x01:
				self.gpio_dio.write(True)
			else:
				self.gpio_dio.write(False)
			data >>= 1
			self.gpio_clk.write(True)

		self.gpio_clk.write(False)
		self.gpio_dio.write(True)
		self.gpio_clk.write(True)
		self.gpio_dio = GPIO(self.dio, "in")

		while self.gpio_dio.read():
			sleep(0.001)
			if self.gpio_dio.read():
				self.gpio_dio = GPIO(self.dio, "out")
				self.gpio_dio.write(False)
				self.gpio_dio = GPIO(self.dio, "in")
		self.gpio_dio = GPIO(self.dio, "out")


def show_ip_address(tm,tmp):
	print(tmp)
	ipaddr = 'smth'
	if tmp==0:
		ipaddr = subprocess.check_output("hostname -I", shell=True).strip()
	else:
		ipaddr = tmp
	print(ipaddr)
	#print("ipaddr={} {}".format(type(ipaddr), ipaddr))
	if (type(ipaddr) is bytes):
		ipaddr=ipaddr.decode('utf-8')
	ipaddr = ipaddr.split(" ")
	ipaddr = ipaddr[0].split(".")
	for octet in ipaddr:
		#print("octet={} [{}]".format(type(octet), octet))
		octet = "   " + octet
		#print("octet={} [{}]".format(type(octet), octet))
		octet = octet[-4:]
		#print("octet={} [{}]".format(type(octet), octet))
		tm.set_segments([0, 0, 0, 0])
		#print("octet[0:1]=[{}]".format(octet[0:1]))
		#print("octet[1:2]=[{}]".format(octet[1:2]))
		#print("octet[2:3]=[{}]".format(octet[2:3]))
		#print("octet[3:4]=[{}]".format(octet[3:4]))
		d0 = 0
		d1 = 0
		d2 = 0
		d3 = 0
		if (octet[0:1] != " "): d0 = tm.digit_to_segment[int(octet[0:1])]
		if (octet[1:2] != " "): d1 = tm.digit_to_segment[int(octet[1:2])]
		if (octet[2:3] != " "): d2 = tm.digit_to_segment[int(octet[2:3])]
		if (octet[3:4] != " "): d3 = tm.digit_to_segment[int(octet[3:4])]
		tm.set_segments([d0, d1, d2, d3])
		sleep(1.0)


def show_clock(tm):
		t = localtime()
		sleep(1 - time() % 1)
		d0 = tm.digit_to_segment[t.tm_hour // 10] if t.tm_hour // 10 else 0
		d1 = tm.digit_to_segment[t.tm_hour % 10]
		d2 = tm.digit_to_segment[t.tm_min // 10]
		d3 = tm.digit_to_segment[t.tm_min % 10]
		tm.set_segments([d0, 0x80 + d1, d2, d3])
		sleep(.5)
		tm.set_segments([d0, d1, d2, d3])

def show_number(tm,num):
		d0 = 0
		d1 = 0
		d2 = 0
		d3 = 0
		if(num <= 9999 and num >=0):
			tmp = False;
			if(num // 1000 != 0):
				d0 = tm.digit_to_segment[num // 1000]
				tmp = True
			if(num // 100 % 10 != 0 or tmp):
				d1 = tm.digit_to_segment[num // 100 % 10]
				tmp = True
			if(num % 100 // 10 != 0 or tmp):
				d2 = tm.digit_to_segment[num % 100 // 10]
				tmp = True
			d3 = tm.digit_to_segment[num % 10]
			num /= 1000
			tm.set_segments([d0, d1, d2, d3])
			return
		
		nums = []
		tmp = False

		if(num<0):
			tmp = True
			num = num * (-1)

		num=str(num)

		while len(num)>0:
			#nums.append(num % 1000)
			#num = num // 1000
			nums.append(num[-3:])
			num = num[:-3]

		nums = list(map(int,nums))		

		tmp1 = False #если хотите чтобы он выводил еще и нолики перед числом, то поставьте True
		for i in range(len(nums),0,-1):
			if tmp: d0 = tm.digit_to_segment[16]
			if (nums[i-1] // 100 != 0 or tmp1):
				d1 = tm.digit_to_segment[nums[i-1] // 100]
				tmp1 = True
			if (nums[i-1] // 10 % 10 != 0 or tmp1):
				d2 = tm.digit_to_segment[nums[i-1] // 10 % 10]
				tmp1 = True
			d3 = tm.digit_to_segment[nums[i-1] % 10]
			tm.set_segments([d0,0x80 + d1, d2, d3])
			sleep(1)
			tm.set_segments([d0, d1, d2, d3])
			sleep(1)
			tmp1 = True;

		
		tm.set_segments([0, 0, 0, 0])

tm = TM1637(CLK, DIO)

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	print("READY!")
	print(publicip.get())

#@client.event
#async def on_message(message):
#	regex = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
#	result_list = re.findall(regex, message.content)
#	print(message.content)
#	result_list = list(set(result_list))
#	if result_list and len(result_list) <= 10:
#		print(result_list)	
#		for ip in result_list:
#			print(ip)

@client.command()
async def dark(ctx,arg1):
	await ctx.send('GHOST! I mean i see '+arg1)
	print(arg1)
	if(arg1=="IP"):	
		print(arg1)
		show_ip_address(tm,0)
		await ctx.send('Bot set IP on 4-digit display')
	elif(arg1=="TIME"):
		print(arg1)
		show_clock(tm)
		await ctx.send('Bot set TIME on 4-digit display ')

@client.command()		
async def disp(ctx,arg1,arg2):
	await ctx.send('GHOST! I mean i see '+arg1+' and '+arg2)
	arg2 = int(arg2)
	if(arg1=="SET"):
		print(arg1,arg2)
		show_number(tm,arg2);

@client.command()
async def show(ctx,arg1):
	#await ctx.send('HAH! YOU LITTLE MONKEY!')
	if ctx.author == client.user:
		return
	
	if (arg1=="IP"):
		print(arg1)
		with StringIO() as buffer, redirect_stdout(buffer):
			publicip.get()
			ip = buffer.getvalue().split()[0]
			show_ip_address(tm,ip)
		#await ctx.send("The server ip is " + ip)


@client.command()
async def test(ctx, member: discord.Member):
	await ctx.send("The id....")
	await ctx.send(f'ID: {member.id}')
	await ctx.send(f'Name: {member.name}')
	await ctx.send(f'NIK: '+str(member));
	arg = int(str(member)[-4:])
	print(arg)
	show_number(tm,arg);

#if __name__ == "__main__":
	#try:
	#	while True:
	#		show_ip_address(tm)
	#		show_clock(tm)
	#		sleep(2.0)
	#except KeyboardInterrupt:
	#	pass

client.run('')

print('cleanup')
gpio_clk.close()
gpio_dio.close()
