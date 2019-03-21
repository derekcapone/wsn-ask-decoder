"""
This script is used decode the binary in the sampled ASK array
This is used assuming that:
 - Preamble and start symbol is removed from signal array
 - Bit length in samples is calculated
 - array starts at beginning of "Count" section of frame
"""

import scipy
import _tkinter
import matplotlib.pyplot as plt


symbols = [0xd,  0xe,  0x13, 0x15, 0x16, 0x19, 0x1a, 0x1c,
           0x23, 0x25, 0x26, 0x29, 0x2a, 0x2c, 0x32, 0x34]

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
