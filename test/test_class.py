
class A(object):
    def _spam(self):
        print 'A._spam'

    def spam(self):
        print 'A.spam'


class B(A):
    def spam(self):
        self._spam()

b = B()
b.spam()

print u'\u4e3b\u4eba\u4e0d\u5728\u5bb6 \u5ba0\u7269\u79f0\u5927\u738b 39'
print u'\u7efc\u827a'
print u'\u7ec8\u6781\u4e09\u56fd2017'
print u'\u6233\uff01\u4e3b\u6f14\u8bbf\u8c08\u82b1\u7d6e'