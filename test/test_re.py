import re



contents = '<style type="text/css" media="all">@import "/web/20120827015302cs_/http://www.fineartsbd.com/files/css/e19640be684861cf88d01a9d15e61f63.css";</style>'

# contents = re.sub(r'<style type="text/css".*?>@import.*?(/web.*?css)";</style>',
#                   '<link rel="stylesheet" type="text/css" href="\1" />',contents)

# contents = re.sub(r'<style type="text/css".*?>@import "(/web.*?\.css)";</style>',
#                   '\1',contents)

# result = re.findall(r'<style type="text/css".*?>@import "(/web.*?\.css)";</style>', contents)
# print(result)
#
# print(contents)

result = re.sub(r'(/web.*?\.css)',
                  r'<link \1>',contents)
print(result)
print(contents)