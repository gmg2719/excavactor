#!/usr/bin/env python

from socket import *
import os,sys,time
import RPi.GPIO as GPIO

HOST = '0.0.0.0'
PORT = 9999

def handle_msg(recv_msg):
    if recv_msg.find("FORWARD")>=0:
        print "Go to front."
        GPIO.output(31,GPIO.LOW)
        GPIO.output(33,GPIO.HIGH)
        GPIO.output(35,GPIO.LOW)
        GPIO.output(37,GPIO.HIGH)
        pass
    if recv_msg.find("BACK")>=0:
        print "Go back"
        GPIO.output(31,GPIO.HIGH)
        GPIO.output(33,GPIO.LOW)
        GPIO.output(35,GPIO.HIGH)
        GPIO.output(37,GPIO.LOW)

    if recv_msg.find("RIGHT")>=0:
        print "Turn right"
        GPIO.output(31,GPIO.LOW)
        GPIO.output(33,GPIO.LOW)
        GPIO.output(35,GPIO.HIGH)
        GPIO.output(37,GPIO.LOW)

    if recv_msg.find("LEFT")>=0:
        print "Turn left"
        GPIO.output(31,GPIO.HIGH)
        GPIO.output(33,GPIO.LOW)
        GPIO.output(35,GPIO.LOW)
        GPIO.output(37,GPIO.LOW)

    if recv_msg.find("DIG")>=0:
        print "Dig dig dig ..."
        GPIO.output(11,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)

    if recv_msg.find("LIFT")>=0:
        print "Lift"
        GPIO.output(11,GPIO.HIGH)
        GPIO.output(13,GPIO.LOW)
    time.sleep(0.1)     
    #Reset all
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(31,GPIO.LOW)
    GPIO.output(33,GPIO.LOW)
    GPIO.output(35,GPIO.LOW)
    GPIO.output(37,GPIO.LOW)
    
    pass

def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(31,GPIO.OUT)
    GPIO.setup(33,GPIO.OUT)
    GPIO.setup(35,GPIO.OUT)
    GPIO.setup(37,GPIO.OUT)

    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(31,GPIO.LOW)
    GPIO.output(33,GPIO.LOW)
    GPIO.output(35,GPIO.LOW)
    GPIO.output(37,GPIO.LOW)
    pass

print "Server started..."
print "Init GPIO..."
init_gpio()
print "Init UDP Server..."
s = socket(AF_INET,SOCK_DGRAM)
s.bind((HOST,PORT))
print 'Waiting for message..'
while True:
    data,address = s.recvfrom(1024)
    print data,address
    handle_msg(data)
    #s.sendto('this is the UDP server',address)
s.close()
