#-*- coding: UTF-8 -*-
import os
import random
import time
import re
from PIL import Image

def remove_html_tags(text):
	"""Remove html tags from a string"""
	clean = re.compile('<.*?>')
	return re.sub(clean, '', text)

def randomDate(start, end, format, prop):
	"""Generate a random date between two other dates"""
	stime = time.mktime(time.strptime(start, format))
	etime = time.mktime(time.strptime(end, format))
	
	ptime = stime + prop * (etime - stime)
	
	return time.strftime(format, time.localtime(ptime)) 

def cropImage(image ,width ,height):
	"""Crop the image starting in the center"""
	img_dir = os.path.dirname(image)
	img_name , img_name_extension = os.path.basename(image).split('.')
	img_target_name = '%s_%dx%d.%s' % (img_name ,width ,height ,img_name_extension)
	img_target_path = os.path.join(img_dir, img_target_name)

	img = Image.open(image)
	half_the_width = img.size[0]/2
	half_the_height = img.size[1]/2
	if img.size[0] < width or img.size[1] < height:
		img_target = img.resize((width,height))
	else:
		img_target = img.crop((half_the_width - width/2 , half_the_height - height/2, half_the_width + width/2, half_the_height + height/2))
	img_target.save(img_target_path)
	
	return img_target_name

def getInstance(themePath, instance):
	overPath = os.path.join(themePath, 'over')
	if not os.path.exists(overPath):
		os.makedirs(overPath)
	return os.path.join(overPath, instance)
	
def AutoSitemap(themePath):
	overPath = os.path.join(themePath, 'over')
	sitemap = []
	for file in os.listdir(overPath):
		if os.path.isfile(os.path.join(overPath,file)) == True:
			sitemap.append(file)
	with open(os.path.join(overPath,'sitemap.txt'),'w') as sitemap_handler:
		for url in sitemap:
			sitemap_handler.write(url + '\n')
	
def generateTemplateFile(themePath, template_handler, instance_handler, title, content = ''):
	templatePath = os.path.join(themePath,'template')
	detailList = [x for x in os.listdir(themePath) if os.path.isfile(os.path.join(themePath,x))]
	for line in template_handler:
		if '{{ title }}' in line:
			instance_handler.write(line.replace('{{ title }}',title))
		elif '{{ content }}' in line:
			instance_handler.write(line.replace('{{ content }}',content))
		elif '<% category_snippet.html %>' in line:
			replace_category_snippet = ''
			with open(os.path.join(templatePath,'category.txt')) as category_handler:
				category = [x.strip() for x in category_handler]
			with open(os.path.join(templatePath,'category_snippet.html')) as category_snippet_handler:
				category_snippet = category_snippet_handler.read()
				for link in category:
					replace_category_snippet += category_snippet.replace('{{ category.href }}',link).replace('{{ category.name }}',link.replace('.html','').replace('-',' '))
			instance_handler.write(line.replace('<% category_snippet.html %>',replace_category_snippet))
		elif '<%' in line and '%>' in line:
			repeat_file_template = line[line.find('<%') + len('<%'):line.find('|')].strip()
			repeat_times = int(line[line.find('| repeat:') + len('| repeat:'):line.find('; %>')].strip())
			
			repeat_file_section = ''
			if repeat_times > len(detailList):
				repeat_file_list = detailList + random.sample(detailList,repeat_times - len(detailList))
			else:
				repeat_file_list = random.sample(detailList,repeat_times)
			repeat_file_imgs = {}
			repeat_file_description = {}
			
			for repeat_file in repeat_file_list:
				with open(os.path.join(themePath,repeat_file)) as repeat_file_handler:
					repeat_file_content = repeat_file_handler.read()
					img_reg = re.compile(r'src=["\'](.+?)["\']')
					img_list = img_reg.findall(repeat_file_content)
					repeat_file_imgs[repeat_file] = img_list
					repeat_file_description[repeat_file] = remove_html_tags(repeat_file_content).split('.')[0].strip()
			
			with open(os.path.join(templatePath,repeat_file_template)) as repeat_file_template_handler:
				repeat_file_template_content = repeat_file_template_handler.read()
				repeat_file_image_section = repeat_file_template_content[repeat_file_template_content.find('{# IMAGE|'):repeat_file_template_content.find('#}') + len('#}')]
				if len(repeat_file_image_section) > 0:
					IMAGE_SIZE = repeat_file_template_content[repeat_file_template_content.find('{# IMAGE|') + len('{# IMAGE|'):repeat_file_template_content.find('#}')]
					IMAGE_WIDTH = int(IMAGE_SIZE[:IMAGE_SIZE.find('x')])
					IMAGE_HEIGHT = int(IMAGE_SIZE[IMAGE_SIZE.find('x') + len('x'):])

			for repeat_file_link in repeat_file_list:
				if len(repeat_file_image_section) > 0:
					repeat_file_img = random.sample(repeat_file_imgs[repeat_file_link],1)[0].split("/")
					repeat_file_img_path = os.path.join(themePath,*repeat_file_img)
				
					repeat_file_img_replace = cropImage(repeat_file_img_path, IMAGE_WIDTH, IMAGE_HEIGHT)
					del repeat_file_img[-1]
					repeat_file_img.append(repeat_file_img_replace)
				else:
					repeat_file_img = []
				
				detailDescription = repeat_file_description[repeat_file_link]
				detailDate = randomDate('January 1, 2016 1:30 PM', 'January 1, 2017 4:50 PM', '%B %d, %Y %I:%M %p', random.random())
				repeat_file_section += repeat_file_template_content.replace('{{ detail.href }}',repeat_file_link)\
					.replace('{{ detail.title }}',repeat_file_link.replace('.html','').replace('-',' '))\
					.replace('{{ time }}',detailDate).replace(repeat_file_image_section,'/'.join(repeat_file_img))\
					.replace('{{ detail.description }}',detailDescription)
					
			instance_handler.write(line.replace(line[line.find('<%'):line.find('%>') + len('%>')],repeat_file_section))
		else:
			instance_handler.write(line)
	
def AutoIndex(themePath):
	templatePath = os.path.join(themePath,'template')
	indexTemplatePath = os.path.join(templatePath,'index.html')
	indexTitle = os.path.basename(themePath)
	
	instance = getInstance(themePath, 'index.html')
	with open(instance,'w') as instance_handler:
		with open(indexTemplatePath) as template_handler:
			generateTemplateFile(themePath ,template_handler ,instance_handler ,indexTitle)
	
def AutoCategory(themePath):
	templatePath = os.path.join(themePath,'template')
	categoryTemplatePath = os.path.join(templatePath,'category.html')
	with open(os.path.join(templatePath,'category.txt')) as category_handler:
		category = [x.strip() for x in category_handler]
	
	for category_link in category:
		categoryTitle = category_link.replace('.html','').replace('-',' ')
		
		instance = getInstance(themePath, category_link)
		with open(instance,'w') as instance_handler:
			with open(categoryTemplatePath) as template_handler:
				generateTemplateFile(themePath ,template_handler ,instance_handler ,categoryTitle)
	
def AutoDetail(themePath):
	templatePath = os.path.join(themePath,'template')
	detailTemplatePath = os.path.join(templatePath,'detail.html')
	
	for file in os.listdir(themePath):
		if os.path.isfile(os.path.join(themePath,file)) == True:
			detailPath = os.path.join(themePath,file)
			detailTitle = file.replace('.html','').replace('-',' ')
			with open(detailPath) as detail_handler:
				detailContent = detail_handler.read()
			
			instance = getInstance(themePath, file)
			with open(instance,'w') as instance_handler:
				with open(detailTemplatePath) as template_handler:
					generateTemplateFile(themePath ,template_handler ,instance_handler ,detailTitle ,detailContent)
			
			

def AutoTheme(theme):
	projetcPath = os.path.dirname(os.path.abspath(__file__))
	themePath = os.path.join(projetcPath,theme)
	AutoDetail(themePath)
	AutoCategory(themePath)
	AutoIndex(themePath)
	AutoSitemap(themePath)

if __name__ == "__main__":
	theme = 'www.mermaidlooks.com'
	AutoTheme(theme)