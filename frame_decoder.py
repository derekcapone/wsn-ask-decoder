import signal_find as sf
import bin_decoder as bd


def checksum_calc(arr):
    sum = 0
    for byte in arr:
        sum += byte
    return sum % 256


file_name = "sig_file.dat"

binary_arr = sf.get_bin_array(file_name)
count, binary_arr = bd.decode_byte(binary_arr)



