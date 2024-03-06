import os
import time
import serial
import cv2 as cv
import file_read
import dijkstra
import dijkstra_head

#Serial Setup
py_serial = serial.Serial(port = '/dev/ttyUSB6', baudrate = 9600)

#Camera Setup
picture = "fswebcam --no-banner --set brightness=10% Images/test1.jpg"
os.system(picture)
img = cv.imread("Images/test1.jpg", cv.IMREAD_COLOR)
resize_img = cv.resize(img, (1020,720), interpolation=cv.INTER_AREA)
cv.imwrite("Images/test1.jpg", resize_img)

#Image Analysis
yolo = "python3 ~/workspace/2D_Waste_Sorting_Solution/detect.py > ~/workspace/2D_Waste_Sorting_Solution/output.txt --weights ~/workspace/2D_Waste_Sorting_Solution/best.pt --img 640 --conf 0.4 --source ~/workspace/2D_Waste_Sorting_Solution/Images/test1.jpg"
os.system(yolo)
time.sleep(1)

#object list
lines = open('~/workspace/2D_Waste_Sorting_Solution/output.txt').readlines()
given_map=file_read.map()
start_row = 0
start_col = 0

while True :
	#Make move order from start position
	move_order, given_map, start_row, start_col, pet_list, can_list = dijkstra.main(given_map, start_row, start_col)
	#Case : detect object = 0 -> head move to initial position and break
	if (len(pet_list) == 0 and len(can_list) == 0):
		move_order = dijkstra_head.main(given_map, start_row, start_col)
		while len(move_order):
			py_serial.write(move_order.pop(0))
			print("pop")
			time.sleep(1.0)
		print("FINISH!")
		break
	#Send order to Arduino using pyserial
	while len(move_order):
		py_serial.write(move_order.pop(0))
		print("pop")
		time.sleep(1.0) #delay time decided by velocity and distance
	
		

