import time
import psycopg2
CONN_STR = "postgresql://perryxiao:v2_3vwNb_3Pa8LFhZpKjtz5sKF8hiiMn@db.bit.io/perryxiao/Audiowings?sslmode=require"
conn = psycopg2.connect(CONN_STR)
cur = conn.cursor()

def get_data():
  sql="""
         SELECT * FROM ppg;
      """
     
  cur.execute(sql)
  conn.commit()

  rv = cur.fetchall()
  #print(f'{rv}')
  print(type(rv))

  x = []
  y = []
  for s in rv:
    #print(s[0],s[1],s[2])
    x.append(s[1])
    y.append(s[2])
  return x,y


x,y = get_data()

import matplotlib.pyplot as plt
# enable interactive mode
plt.ion()
 
# creating subplot and figure
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y)
plt.xlabel ('Time [s]')
plt.ylabel ('PPG Singal [a.u.]')
title = 'Heart Rate PPG' 
plt.title(title)

# looping
for _ in range(5):
    x,y = get_data()
    # updating the value of x and y
    line1.set_xdata(x)
    line1.set_ydata(y)
 
    # re-drawing the figure
    fig.canvas.draw()
     
    # to flush the GUI events
    fig.canvas.flush_events()
    time.sleep(5)
    
