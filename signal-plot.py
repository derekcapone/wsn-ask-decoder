import matplotlib.pyplot as plt
import scipy

f_name = "test-signal.txt"

first_sig = scipy.fromfile(open("sig_file2.dat"), dtype=scipy.float32)
signal = scipy.fromfile(open("sig_file.dat"), dtype=scipy.float32)

plt.subplot(2,1,1)
plt.plot(first_sig)

plt.subplot(2,1,2)
plt.plot(signal)

plt.show()
