import serial
import math
import csv
import time
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y-%H:%M:%S")

port = '/dev/ttyACM1'

usbacc = serial.Serial(port)

# CHANGE RANGE TO +- 2
RANGE = 4
FREQ = 100
g = 9.80665 # VALUE OF G IN METERS PER SECOND SQUARE

def csv_to_2D_list(csv_list):
	# YOU CAN USE acc_sample.strip() OR acc_sample[0:-2]
	return [list(map(float, acc_sample[0:-5].split(','))) for acc_sample in csv_list]

range_write = 'RANGE ' + str(RANGE)
usbacc.write(range_write.encode())

freq_write = 'FREQ ' + str(FREQ)
usbacc.write(freq_write.encode())

# READ N SAMPLES
n_samples = 50

with open("/home/weihan08/Desktop/AccelerometerData/"+ dt_string + ".csv","a+") as csvfile:
	sensorwriter = csv.writer(csvfile, delimiter=',') 
	sensorwriter.writerow(['Time','Acceleration'])

	try:
		while True:
			input_csv = []
			for _ in range(n_samples):
				input_csv.append(str(usbacc.readline())[2:])
			acc = csv_to_2D_list(input_csv)

	# CALCULATE AVERAGE ACCELERETION IN m/s^2
			accx_avg = 0.0
			accy_avg = 0.0
			accz_avg = 0.0

			for sample in acc:
				# print(sample)
				accx_avg += sample[0]
				accy_avg += sample[1]
				accz_avg += sample[2]

			accx_avg = accx_avg / n_samples
			accy_avg = accy_avg / n_samples
			accz_avg = accz_avg / n_samples

	# CALCULATE TOTAL AVERAGE ACCELERATION, remove constant gravity -9.13.
		#	Total_acc = g * math.sqrt(accx_avg**2 + accy_avg**2 + accz_avg**2) * (RANGE / 511.5) - 9.13 #10-bit resolution, should divide by 1023, but since range is +/-, so *2/1023=1/511.5
			Total_acc = math.sqrt(accx_avg**2 + accy_avg**2 + accz_avg**2) * (RANGE / 511.5) - 0.928  #10-bit resolution, should divide by 1023, but since range is +/-, so *2/1023=1/511.5
			print('\nTotal average acceleration is equal ' + str(Total_acc) + ' G forces')
			now = datetime.now()
			y=[str(now.strftime("%d-%m-%Y-%H:%M:%S")),str(Total_acc)]
			sensorwriter.writerow(y)
			csvfile.flush()
			
	except KeyboardInterrupt:
		usbacc.close() # CLOSE USB CONNECTION
		print('Interrupted!')




