import csv

with open('some.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows([('95270a15f78a240dc6ab7f4daee44d45.jpg', '309256_12.jpg', '309256', '/data/www/image.app/upload/36/2'),('95270a15f78a240dc6ab7f4daee44d45.jpg', '309256_12.jpg', '309256', '/data/www/image.app/upload/36/2')])