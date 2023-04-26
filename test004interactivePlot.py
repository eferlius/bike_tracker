import matplotlib.pyplot as plt
import numpy as np

# x = np.linspace(0, 6*np.pi, 100)
# y = np.sin(x)

# # You probably won't need this if you're embedding things in a tkinter plot...
# plt.ion()

# fig = plt.figure()
# ax = fig.add_subplot(111)
# line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

# for phase in np.linspace(0, 10*np.pi, 500):
#     line1.set_ydata(np.sin(x + phase))
#     fig.canvas.draw()
#     fig.canvas.flush_events()


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
x = 0
y = 0

line1, = ax1.plot(x,y,'r-')
line2, = ax2.plot(x,y,'b-.')
ax1.grid(True)
ax2.grid(True)


for i in np.arange(0,11,0.1):
    x = np.arange(0,i,0.1)
    y = x+np.random.rand(len(x))

    line1.set_xdata(x)
    line1.set_ydata(y)
    if len(x)>10:
        line2.set_xdata(x[-10:])
        line2.set_ydata(y[-10:])
        ax1.set_xlim([np.min(x), np.max(x)])
        ax1.set_ylim([np.min(y), np.max(y)])
        ax2.set_xlim([np.min(x[-10:]), np.max(x[-10:])])
        ax2.set_ylim([np.min(y[-10:]), np.max(y[-10:])])
    else:
        line2.set_xdata(x)
        line2.set_ydata(y)



    #ok = input('press any key to continue...')
    fig.canvas.draw()
    fig.canvas.flush_events()
