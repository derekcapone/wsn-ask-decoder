import matplotlib.pyplot as plt
import scipy

f_name = "test-signal.txt"

first_sig = scipy.fromfile(open("sig_file2.dat"), dtype=scipy.float32)
second_sig = scipy.fromfile(open("sig_file1.dat"), dtype=scipy.float32)
signal = scipy.fromfile(open("sig_file.dat"), dtype=scipy.float32)

plt.subplot(3,1,1)
plt.plot(first_sig[713248:2312900])
plt.title("After Complex to Real Block")

plt.subplot(3,1,2)
plt.plot(second_sig[713248:2312900])
plt.title("After RMS Block")

plt.subplot(3,1,3)
plt.plot(signal[713248:2312900])
plt.title("Final signal")

plt.show()
