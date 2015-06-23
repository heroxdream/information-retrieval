__author__ = 'hanxuan'

from struct import pack, unpack

def vb_encode(numbers):
    bytes_total = []
    for number in numbers:
        bs = []
        while True:
            bs.insert(0, number % 128)
            if number < 128:
                break
            number /= 128
        bs[-1] += 128
        print bs
        bytes_total += bs
    return pack('%dB' % len(bytes_total), *bytes_total)

def vb_decode(bytestream):
    n = 0
    numbers = []
    bytestream = unpack('%dB' % len(bytestream), bytestream)
    for byte in bytestream:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            numbers.append(n)
            n = 0
    return numbers


if __name__ == '__main__':
    # numbers = [1, 12, 45, 23, 160968, 1, 56, 34, 84678, 27]
    numbers = [160968]
    # print vb_decode(vb_encode(numbers))
    print len(vb_encode(numbers))
