
# import struct


# output = open('./test', 'wb')
# num = [12, 14, 15, 16]
#
# b2 = struct.pack('4H', *num)
#
# print 'b2.len: {}'.format(len(b2))
#
# b3 = struct.unpack('Ibh', b2[13:20])
#
# b3 = struct.unpack_from('I', b2, 13)
#
# print b3
#
# output.write(b2)
# print output.tell()
# output.close()


# fmt = ''.join(['I', 'H'])
#
# print fmt
#
# num1 = 1769824134
# num2 = 123
# b2 = struct.pack(fmt, num1, num2)
# output.write(b2)
# print output.tell()
# output.close()


from Index.CacheReader import CacheReader
# input_file = open('./Index/IndexFile/2.index', 'rb')
# # 3IIBHIBH
# input_file.seek(160)
# b = input_file.read(24)
# print input_file.tell()
# num2 = struct.unpack('6I', b)
# print struct.calcsize('3IIIIIII3IIIIIIIII3IIIIIIIII3IIIIIII3IIII3IIII3IIII3IIII3IIII3IIII')
# print struct.calcsize('3IIB')
# print struct.calcsize('H')
# print num2

# d = CacheReader(num2).read_all()
# for token in d:
#     print token, ': ', d[token]





#
# input_file.seek(4)
# b = input_file.read()
#
# seq = struct.unpack('I', b)
# print(seq)

# a='hello'
#
# b='world!'
#
# c=2
#
# d=45.123
#
# bytes=struct.pack('5s6sif',a,b,c,d)
#
#
# a1,b1,c1,d1=struct.unpack('5s6sif',bytes)
#
# print a1, b1, c1, d1
#
# num = [4294967295,14,15,16,17]
#
# b2 = struct.pack('5I', *num)
#
# ba = bytearray(b2)
#
# print struct.unpack('I', ba[0:4])

#
# import collections
#
# d = {'a':(0,3), 'b':(3,1), 'c':(4, 4)}
#
# dd = dict()
# for k in d:
#     dd[k] = d[k][1]
#
# dd = collections.Counter(dd)
# for k,v in dd.most_common(len(dd)):
#     print k, v

#
# for i in range(0, 100):
#     print struct.calcsize('{}s'.format(i))


# import array

# a = array.array('H', xrange(10))
# print a.buffer_info()
# print a.buffer_info()[1] * a.itemsize


# b = array.array('I', xrange(10))
#
# a.extend(b)



# print len(bytearray(a))

# a.byteswap()



# def vb_encode(number):
#     bytes = []
#     while True:
#         bytes.insert(0, number % 128)
#         if number < 128:
#             break
#         number /= 128
#     bytes[-1] += 128
#     return pack('%dB' % len(bytes), *bytes)


# def vb_encode(number):
#     bytes = []
#     while True:
#         bytes.insert(0, number % 128)
#         if number < 128:
#             break
#         number /= 128
#     bytes[-1] += 128
#     return pack('%dB' % len(bytes), *bytes)

#
# import sys
#
# import heapq as queue
#
# span = sys.maxint
# heap = [2, 4, 5, 6, 12, 45, 56]
# heap.reverse()
# queue.heapify(heap)
# while heap:
#     print queue.heappop(heap)
#
# queue.heappop(heap)
#
# heads = [None] * 10
#
# print heads



from collections import defaultdict

d = defaultdict(set)

d[1].add(11)
d[1].add(12)
d[2].add(21)
d[3].add(31)
d[3].add(32)

print d














