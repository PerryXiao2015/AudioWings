import time
import board
import busio

# pip install psycopg2==2.7.5
# python -m pip install psycopg2-binary 

import psycopg2
CONN_STR = "postgresql://perryxiao:v2_3vwNb_3Pa8LFhZpKjtz5sKF8hiiMn@db.bit.io/perryxiao/Audiowings?sslmode=require"
conn = psycopg2.connect(CONN_STR)
cur = conn.cursor()


import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
# Data rate must be one of: [128, 250, 490, 920, 1600, 2400, 3300]
ads = ADS.ADS1015(i2c,gain=2,data_rate=2400)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

def get_data(n):
	x_values = []      # Time stamp dt
	y_values = []      # ECG output signal
	y1_values = []     # ECG LO-
	y2_values = []     # ECG LO+
	y3_values = []     # PPG signal

	i = 0

	t0 = int(time.time() * 1000)
	print("Time in milliseconds since epoch", t0)

	while (i < n):
		t1 = int(time.time() * 1000) - t0
		x_values.append(t1 )
		i = i + 1
		y_values.append(chan0.voltage)
		y1_values.append(chan1.voltage)
		y2_values.append(chan2.voltage)
		y3_values.append(chan3.voltage)
		#print("Time {:>5.5f} Chan0 {:>5.3f} Chan1 {:>5.3f} Chan2 {:>5.3f} Chan3 {:>5.3f}".format(t1, chan0.voltage,chan1.voltage,chan2.voltage,chan3.voltage))
		time.sleep(0.001)

	# Save data to local CSV file =============================================
	#a = open('test20221122.csv', 'w')
	#a.write("t,Chan0(ECG output), Chan1(ECG LO-), Chan2(ECG LO+), Chan3(PPG)\n")
	#for j in range(i):
	#	a.write("{:>5.4f},{:>5.4f},{:>5.4f},{:>5.4f},{:>5.4f}\n".format(x_values[j],y_values[j],y1_values[j],y2_values[j],y3_values[j]))
	#a.close()

	#==========================================================================
	# Save data in database
    print("Saving data to database ... ")
	sql="""
		   TRUNCATE TABLE ppg RESTART IDENTITY;
		"""
	cur.execute(sql)

	for x,y3 in zip(x_values,y3_values):                     # Initialize for loop
		#print('Index', i, '- t:', row['t'], '- Chan3(PPG):', row[' Chan3(PPG)'])
		sql = "INSERT INTO ppg (time, ppg) VALUES (%s, %s)" % (x, y3)
		cur.execute(sql)

	conn.commit()

	'''
	sql="""
		   SELECT * FROM ppg;
		"""

	cur.execute(sql)

	conn.commit()

	rv = cur.fetchall()
	#print(f'{rv}')
	'''

for i in range(10):
    get_data(250)
	
# Disconnect the database
cur.close()
conn.close()