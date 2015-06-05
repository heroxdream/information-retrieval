
import struct


# output = open('./test', 'wb')
# num = [12,14,15,16,17]
#
# b2 = struct.pack('5I', *num)
#
# b3 = struct.unpack('5I', b2)
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
input_file = open('./Index/IndexFile/2.index', 'rb')
# # 3IIBHIBH
input_file.seek(160)
b = input_file.read(24)
# print input_file.tell()
num2 = struct.unpack('6I', b)
# print struct.calcsize('3IIIIIII3IIIIIIIII3IIIIIIIII3IIIIIII3IIII3IIII3IIII3IIII3IIII3IIII')
# print struct.calcsize('3IIB')
# print struct.calcsize('H')
# print num2

d = CacheReader(num2).read_all()
for token in d:
    print token, ': ', d[token]





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
