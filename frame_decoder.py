import signal_find as sf
import bin_decoder as bd


class Frame:
    dev_num = None
    dev_type = None
    maint_num = None
    payload = None


def frame_decode(payload):
    dev_num_size = 2
    dev_type_size = 1
    maint_size = 1
    payload_size = 1
    rec_frame = Frame()

    rec_frame.dev_num = payload[:dev_num_size]
    print(rec_frame.dev_num)


def checksum_calc(arr):
    sum = 0
    for byte in arr:
        sum += byte
    return sum % 256


file_name = "sig_file.dat"

binary_arr = sf.get_bin_array(file_name)
count, binary_arr = bd.decode_byte(binary_arr)
payload = bd.get_bytes(binary_arr, count)
frame_decode(payload)


