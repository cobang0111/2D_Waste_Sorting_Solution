## <div align="center">2023-1 서강 융합기술 경진대회 </div>
🚀 yolov5 모델을 활용한 재활용품 분류 SW 및 장치

## <div align="center">Team 서계</div>
🌟 Team Leader 이창재 (서강대학교 기계공학과 19)

🌟 Team member 강정훈 (서강대학교 기계공학과 19)

🌟 Team member 김기훈 (서강대학교 기계공학과 / 컴퓨터공학과 19)

🌟 Team member 이도헌 (서강대학교 기계공학과 19)

## <div align="center">Video</div>

🚀 See our operation video on the YouTube

[Youtube_link](https://www.youtube.com/watch?v=P4Z1LM5an2k)

![image](https://github.com/cobang0111/2D_Waste_Sorting_Solution/assets/97373900/ff19f49e-b665-49a0-aad7-9d098a361ac1)


## <div align="center">Summary</div>

Raspberry Pi4에서 WebCam 으로 분류 Desk를 촬영합니다.

![image](https://github.com/cobang0111/2D_Waste_Sorting_Solution/assets/97373900/780a27f5-6a42-4bd6-93d0-95aec734a358)

<br>

이를 customized YOLO 로 분석하고, 분석된 이미지를 Matrix 에 Mapping 합니다.

![image](https://github.com/cobang0111/2D_Waste_Sorting_Solution/assets/97373900/67a236b9-3df1-4eb4-bbfe-f0d4f39e5ef7)


<br>

이를 Dijkstra Algorithm을 이용하여 최적 경로를 계산하고 2D 플로터를 사용하여 분류합니다.
<br>
이 Repository 는 모형 캔과 모형 페트에 대해 YOLO를 customizing 시켰고,
<br>
페트 모형을 위쪽으로, 캔 모형을 아래로 분류합니다. 
<br>

## <div align="center">Pre-requisite</div>


🚀 Customized yolov5 using Roboflow and Google Colab

- [Our Roboflow Data Set](https://app.roboflow.com/sgme/classify-pet-and-can/4)

- Dataset 을 사용하여 Google Colab 에서 custom 분석 모델을 학습시킵니다. 

- 높은 정확도와 빠른 분석을 위하여 yolov5m 모델을 이용하여 [best.pt](https://drive.google.com/file/d/1xFNFxLWNwAg3CrGFe8cWR2mcu1oUs7Ly/view?usp=sharing)를 제작

- 본인의 workspace 디렉토리를 만들고 해당 디렉토리에서 이 repository를 git clonning 합니다.

```bash

cd ~/workspace

git clone https://github.com/cobang0111/2D_Waste_Sorting_Solution.git

```

<br>

## <div align="center">Execution</div>


Integration Code 인 recycle.py를 작동시키면, 촬영부터, 분석 및 실행까지 한 번에 작업이 통합되어 수행됩니다.

integration code에서 baudrate와 output.txt 파일의 경로를 적절히 수정해야 합니다.

	
🚀 Integration Code - Python3 Code (recycle.py)

<p align = "center"> recycle.py </p>

```python
import os
import time
import serial
import cv2 as cv
import file_read
import dijkstra

#Serial Setup
py_serial = serial.Serial(port = '/dev/ttyUSB0', baudrate = 9600)

#Camera Setup
picture = "fswebcam --no-banner --set brightness=60% Images/test1.jpg"
os.system(picture)
img = cv.imread("Images/test1.jpg", cv.IMREAD_COLOR)
resize_img = cv.resize(img, (1020,720), interpolation=cv.INTER_AREA)
cv.imwrite("Images/test1.jpg", resize_img)

#Image Analysis
yolo = "python3 2D_Waste_Sorting_Solution/detect.py > 2D_Waste_Sorting_Solution/output.txt --weights 2D_Waste_Sorting_Solution/best.pt --img 640 --conf 0.4 --source Images/test1.jpg"
os.system(yolo)
time.sleep(1)

# object list
# You need to modify here
lines = open('~/workspace/2D_Waste_Sorting_Solution/output.txt').readlines()
given_map=file_read.map()
start_row = 0
start_col = 0

while True :
	#Make move order from start position
	move_order, given_map, start_row, start_col, pet_list, can_list = dijkstra.main(given_map, start_row, start_col)
	if (len(pet_list) == 0 and len(can_list) == 0):
		print("FINISH\n")
		break
	
	while len(move_order):
		py_serial.write(move_order.pop(0))
		print("pop")
		time.sleep(1.0) #delay time decided by velocity and distance		
	
```

<br>

적절히 수정을 하였다면 아래 명령어로 작동시킬 수 있습니다.

```bash

cd ~/workspace

python3 recycle.py

```

<br>
<br>
<br>

			  
## <div align="center">Reference - yolov5</div>

See the [YOLOv5 Docs](https://docs.ultralytics.com/yolov5) for full documentation on training, testing and deployment. 

