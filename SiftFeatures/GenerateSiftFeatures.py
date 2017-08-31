#-*- coding: UTF-8 -*-

import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ImageFingerprint')


inputPath = '/data/dev-crawler/sift-database/ucenterdress.csv'
imageList = []

with open(inputPath) as f:
	for line in f:
		data = line.split(',')
		if len(data) == 6:
			image = data[3].strip()

			color_image = cv2.imread(image)


			def to_gray(color_img):
				gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
				return gray

			gray_image = to_gray(color_image)	
				
			def gen_sift_features(gray_img):
				sift = cv2.xfeatures2d.SIFT_create()
				# kp is the keypoints
				#
				# desc is the SIFT descriptors, they're 128-dimensional vectors
				# that we can use for our final features
				kp, desc = sift.detectAndCompute(gray_img, None)
				return kp, desc

			# generate SIFT keypoints and descriptors
			kp, desc = gen_sift_features(gray_image)

			desc_list = desc.tolist()

			descLength = len(desc_list)
			print descLength

			itemDict = {
				'owner': 'ucenterdress',
				'name': data[1],
				'path': data[3],
				'sn': data[0],
				'date': '2017-02-21',
			}
			for i in range(descLength/100 + 1):
				if (i+1)*100 <= descLength:
					offset = (i+1)*100
				else:
					offset = descLength
				itemDict[ 'fingerprint%s' % (i+1) ] = json.dumps(desc_list[i*100 : offset])
			table.put_item(Item = itemDict)
			
			#print type(json_desc)

			#json_list_desc = json.loads(json_desc)

			#print type(json_list_desc)
			
