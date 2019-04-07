"""
This script is used to:
 - decode the binary in the sampled ASK array
 - calculates the byte information from binary array
This is used assuming that:
 - Preamble and start symbol is removed from signal binary array
 - Bit length in samples is calculated
"""

# reverse table to convert back to bytes from 6 bit chunks
reverse_symbols = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 1, 0, 0, 0, 0, 2,
                   0, 3, 4, 0, 0, 5, 6, 0, 7, 0,
                   0, 0, 0, 0, 0, 8, 0, 9, 10, 0,
                   0, 11, 12, 0, 13, 0, 0, 0, 0, 0,
                   14, 0, 16]


def decode_byte(bin_arr):
    """
    Converts next 12-bits of binary array into byte of data
    :param bin_arr: binary array of samples
    :return: decoded byte, signal array with 12 bits removed
    """
    low_nib = 0
    high_nib = 0
    for i in range(6):
        high_nib += bin_arr[i] * (2**i)
        low_nib += bin_arr[i+6] * (2**i)

    # convert to low and high 4-bits from lookup table
    byte = (reverse_symbols[high_nib] << 4) | reverse_symbols[low_nib]

    return byte, bin_arr[12:]


def get_bytes(binary_arr, count):
    """
    Decodes the binary array to get array of bytes
    :param binary_arr: binary array of signal
    :param count:
    :return:
    """
    payload = []
    for i in range(0, count):
        byte, binary_arr = decode_byte(binary_arr)
        payload += [byte]
    return payload
