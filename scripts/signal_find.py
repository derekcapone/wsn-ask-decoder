"""
This script performs the following functions:
 - Reads the raw signal samples into an array
 - finds the beginning of the signal
 - Calculates the bit length in samples
 - Checks the preamble to ensure the signal is valid
 - Converts the signal into a binary array
"""

import scipy
import sys

preamble_length = 35  # preamble length
exp_preamble = [1, 0, 1, 0, 1, 0,  # expected preamble
                1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1]


def get_raw_signal(f_name):
    """ returns signal samples in form of an array """
    return scipy.fromfile(open(f_name), dtype=scipy.float32)


def get_bit_length(raw_sig):
    """
    - finds bit length in samples
    - removes non-signal samples at beginning of array
    :param raw_sig: array of signal samples
    :return: bit length in samples, signal array starting at preamble
    """
    state = 0 # start in zero state
    for i in range(0, len(raw_sig)):
        if state is 0 and raw_sig[i] > 0.5:
            # find beginning of signal
            beg_sig = i
            state = 1
        elif state is 1 and raw_sig[i] < 0.5:
            # find bit length
            bl = i - beg_sig
            break

    return bl, raw_sig[beg_sig+10:]  # note the plus 10 is to start in state for active bit


def check_preamble(preamble):
    """
    Checks if preamble is correct
    :param preamble: preamble array
    :return: True if correct, False if incorrect
    """
    return preamble == exp_preamble


def sample_signal(raw_sig, bit_len):
    """
    Generates binary array by finding state changes in signal and calculating bits from length
    :param raw_sig: raw signal starting after preamble
    :param bit_len: bit length
    :return: binary array from sampled signal
    """
    bin_arr = []  # create empty array (size of binary array unknown)
    state = raw_sig[0]  # get starting bit state
    start_samp = 0
    for i in range(0, len(raw_sig)):
        if i-start_samp > 4*bit_len:  # end of signal
            bin_arr += [0]*(6-(len(bin_arr[preamble_length:])%6))  # append 0's that were cut off (6-bit chunks)
            break
        if state != raw_sig[i]:
            length = i - start_samp  # length of string of bits
            num_bits = calc_num_bits(bit_len, length)
            bin_arr += [int(state)]*num_bits  # append bits to array
            state = 1 - state  # flip states
            start_samp = i  # reset starting sample
    return bin_arr


def calc_num_bits(bit_len, len):
    return round(len/bit_len)


def get_bin_array(f_name):
    """
    Produces binary array from raw signal input (file)
    Exits the program if preamble is incorrect
    :return: binary array of signal (excluding preamble)
    """
    raw_signal = get_raw_signal(f_name)
    bit_length, raw_signal = get_bit_length(raw_signal)
    bin_arr = sample_signal(raw_signal, bit_length)

    if not check_preamble(bin_arr[:preamble_length]):
        print("Preamble incorrect...")
        sys.exit()
    bin_arr = bin_arr[preamble_length:]  # remove preamble

    return bin_arr
