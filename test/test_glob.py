# coding:utf-8
import glob

#返回的结果是绝对路径列表：指定目录下所有txt文件
print glob.glob('E:/task/*/*.txt')

#返回的结果是相对路径列表：上级目录下所有py文件
print glob.glob('../*.py')


print glob.glob('.?*')