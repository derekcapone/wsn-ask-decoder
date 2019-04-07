import signal_find as sf
import bin_decoder as bd
import sys


# class to hold all frame values
class Frame:
    dev_num = None
    dev_type = None
    maint_num = None
    pl_size = None
    payload = None


def log_frame(frame):
    """ Logs field information to frame_log.txt """
    f = open("../frame_logs.txt", 'a+')
    f.write("Device number: %d\n" % frame.dev_num)
    f.write("Device Type: %d\n" % frame.dev_type)
    f.write("Transmissions since maintenance: %d\n" % frame.maint_num)
    f.write("Monitoring Payload: %s\n\n" % hex(frame.payload))


def frame_decode(pl):
    """
    Decodes the frame from the byte array
    :param pl: byte array (payload)
    :return: frame object with populated fields
    """
    rec_frame = Frame()
    dev_num_size = 2  # size of device number in frame (bytes)

    # extract device number
    rec_frame.dev_num, pl = reconstruct_bytes(pl, dev_num_size)

    # extract device type
    rec_frame.dev_type = pl[0]
    pl = pl[1:]

    # extract maintenance number
    rec_frame.maint_num = pl[0]
    pl = pl[1:]

    rec_frame.pl_size = pl[0]
    pl = pl[1:]

    # extract monitoring payload
    rec_frame.payload = pl[0]
    rec_frame.payload, pl = reconstruct_bytes(pl, rec_frame.pl_size)

    return rec_frame


def reconstruct_bytes(payload, num_bytes):
    """
    Reconstructs fields of frame that are multiple bytes
    :param payload: byte array of signal information
    :param num_bytes: number of bytes in field
    :return: reconstructed byte value, byte array with field removed
    """
    byte_val = 0
    for i in range(0, num_bytes):
        byte_val |= payload[i] << (num_bytes-i-1)*8
    return byte_val, payload[num_bytes:]


def checksum_calc(arr):
    """ Calculates checksum of array """
    sum_val = sum(arr)
    return sum_val % 256


def verify_checksum(payload):
    """ Verifies payload is correct
        Returns True if correct, False otherwise"""
    checksum = payload[-1]
    temp_pl = payload[:-1]
    return checksum == checksum_calc(temp_pl)


file_name = "../signal_files/sig_file.dat"

binary_arr = sf.get_bin_array(file_name)
count, binary_arr = bd.decode_byte(binary_arr)
payload = bd.get_bytes(binary_arr, count)
print(payload)

if not verify_checksum(payload):
    print("Checksum incorrect. Dropping packet...")
    sys.exit()

rec_frame = frame_decode(payload)
log_frame(rec_frame)
