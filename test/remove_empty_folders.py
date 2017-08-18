import os


path = r'E:\task\empty'

# for root, dirs, files in os.walk(path, topdown=False):
#     if not os.listdir(root):
#         os.rmdir(root)
#         print root

for root, dirs, files in os.walk(path, topdown=False):
    print root, dirs, files
    for name in files:
        os.remove(os.path.join(root, name))
    if not files and not dirs:
        os.rmdir(root)
        print 'Removed :', root