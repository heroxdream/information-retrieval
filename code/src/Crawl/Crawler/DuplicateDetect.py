# -*- coding: utf-8 -*-

__author__ = 'hanxuan'
import re
from simhash import Simhash, SimhashIndex


s1 = 'How are you? I Am fine. blar#@ blar#$% blar!$^* blar∑ßå≈©¬…π blar Thanks.'.decode('utf-8', 'ignore')

s2 = 'How are you i am fine. blar blar blar blar blar than'.decode('utf-8', 'ignore')

s3 = 'This is simhash test.'.decode('utf-8', 'ignore')

# print get_features(s1)
#
# print Simhash(get_features('How are you? I am fine. Thanks.')).value


sh1 = Simhash(s1)
sh2 = Simhash(s2)
sh3 = Simhash(s3)

# print sh.value


# print sh1.distance(sh2)

shIndex = SimhashIndex([], k=3)
shIndex.add('1', sh1)
shIndex.add('2', sh2)
# shIndex.add('3', sh3)

if shIndex.get_near_dups(sh3):
    print 'YES'
else:
    print 'NO'

# print shIndex.get_near_dups(sh2)


