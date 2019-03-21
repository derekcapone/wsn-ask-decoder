import scipy
import sys
import signal_find as sf
import bin_decoder as bd


def crc_calc(arr):
    sum = 0
    for byte in arr:
        sum += byte
    return sum % 256


file_name = "0x0102.txt"

binary_arr = sf.get_bin_array(file_name)
count, binary_arr = bd.decode_byte(binary_arr)

payload = []
for i in range(0, count):
    byte, binary_arr = bd.decode_byte(binary_arr)
    payload += [byte]

