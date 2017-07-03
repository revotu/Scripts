# coding:utf-8
import os
import re
import fnmatch
import shutil

def remove_html_tags(text):
	"""Remove html tags from a string"""
	clean = re.compile('<.*?>')
	return re.sub(clean, '', text)

def extractLogo(path):
	dst = 'C:/Users/revotu/Desktop/task_seo/logos/'
	for site in os.listdir(path):
		logos = []
		for root, dirnames, filenames in os.walk(os.path.join(path, site)):
			for filename in fnmatch.filter(filenames, '*logo*.png'):
				logos.append(os.path.join(root, filename))
			for filename in fnmatch.filter(filenames, '*logo*.jpg'):
				logos.append(os.path.join(root, filename))
		for logo in logos:
			if not os.path.exists(os.path.join(dst, site)):
				os.makedirs(os.path.join(dst, site))
			shutil.copy(logo, os.path.join(dst, site, os.path.basename(logo)))

def replaceLogo(sites, logos, replaceFile):
	with open(replaceFile) as f:
		rewriteRules = {}
		for line in f:
			src, dst = line.strip().split('`')
			rewriteRules[src] = dst
			
	for site in os.listdir(logos):
		tmp = site.replace('www.','')
		dstSite = site.replace(tmp,rewriteRules[tmp])
		
		dstPath = os.path.join(sites, dstSite)
		if os.path.exists(dstPath):
			for newLogo in os.listdir(os.path.join(logos, site)):
				for root, dirs, files in os.walk(dstPath):
					if newLogo in files:
						dstLogo = os.path.join(root, newLogo)
						srcLogo = os.path.join(logos, site, newLogo)
						shutil.copy(srcLogo, dstLogo)
						print site,newLogo,dstLogo
				
	

def check_num():
	sitesDir = '/home/zhujun/sites'
	domainFile = 'replace_exact_domain.txt'
	with open(os.path.join(sitesDir,domainFile)) as f:
		domainList = [line.strip() for line in f]
	
	num = 0
	for domain in domainList:
		if os.path.exists(os.path.join(sitesDir,domain)):
			num += 1
		else:
			print domain
	print num

def gen_exact_path():
	sitesDir = '/home/zhujun/sites'
	origFile = '/home/zhujun/sites/replace_domain.txt'
	destFile = '/home/zhujun/sites/replace_exact_domain.txt'
	
	with open(destFile, 'w') as outfile:
		with open(origFile) as infile:
			for f in infile:
				if os.path.exists(os.path.join(sitesDir,f.strip())):
					print f.strip()
					outfile.write(f.strip()+'\n')
				elif os.path.exists(os.path.join(sitesDir,'www.' + f.strip())):
					print 'www.' + f.strip()
					outfile.write('www.' + f.strip()+'\n')

def replaceDomain(path, src, dst):
	with open(path) as f:
		content = f.read()
	
	content_reg = re.compile(re.escape(src), re.IGNORECASE)
	content = content_reg.sub(dst, content)
	content_reg = re.compile(re.escape(src.split('.')[0]), re.IGNORECASE)
	content = content_reg.sub(dst.split('.')[0], content)
	
	with open(path, 'w') as f:
		f.write(content)

def config(sites, replaceFile):
	with open(replaceFile) as f:
		rewriteRules = {}
		for line in f:
			src, dst = line.strip().split('`')
			rewriteRules[src] = dst
			
	for site in os.listdir(sites):
		src = site.replace('www.','')
		if src in rewriteRules:
			dst = rewriteRules[src]
			replaceSite = site.replace(src, dst)
			replaceSitePath = os.path.join(sites,replaceSite)
			os.rename(os.path.join(sites,site),replaceSitePath)
			
			saveFiles = []
			try:
				with open(os.path.join(replaceSitePath, 'sitemap.txt')) as f:
					saveFiles = [line.strip().split('/')[-1] for line in f if len(line.strip()) > 0]
					saveFiles.append('today.txt')
					saveFiles.append('sitemap.txt')
				replaceDomain(os.path.join(replaceSitePath, 'sitemap.txt'), src, dst)
			except:
				print('NO SITEMAP:{}'.format(site))
			
			try:	
				for file in os.listdir(os.path.join(replaceSitePath, 'config')):
					if file not in ['index_template.html','template.html']:
						os.remove(os.path.join(replaceSitePath, 'config', file))
					else:
						replaceDomain(os.path.join(replaceSitePath, 'config', file), src, dst)
			except:
				print('NO CONFIG:{}'.format(site))
			
			for file in os.listdir(replaceSitePath):
				if os.path.isfile(os.path.join(replaceSitePath, file)):
					if any(s in file for s in ('.zip','.bak','.htmlremoved')) or file == 'log':
						os.remove(os.path.join(replaceSitePath, file))
					elif file.endswith(('.html', '.txt')):
						if file not in saveFiles:
							os.remove(os.path.join(replaceSitePath, file))
						else:
							replaceDomain(os.path.join(replaceSitePath, file), src, dst)
					
		elif src in rewriteRules.values():
			if os.path.isdir(os.path.join(sites, 'www.' + src)):
				src = 'www.' + src
			for file in os.listdir(os.path.join(sites, src)):
				if any(s in file for s in ('.remove','.py')):
					os.remove(os.path.join(sites, src, file))
				
		else:
			print('NO SITE:{}'.format(site))

def listPHP(sites):
	for site in os.listdir(sites):
		matches = []
		for root, dirnames, filenames in os.walk(os.path.join(sites, site)):
			for filename in fnmatch.filter(filenames, '*.php'):
				matches.append(os.path.join(root, filename))
		print site, len(matches)
		
def removePHP(sites, phpSite, replaceFile):
	with open(replaceFile) as f:
		rewriteRules = {}
		for line in f:
			src, dst = line.strip().split('`')
			rewriteRules[src] = dst
	with open(phpSite) as f:
		removeSites = [line.strip() for line in f]
	
	for site in removeSites:
		tmp = site.replace('www.','')
		removeSite = site.replace(tmp,rewriteRules[tmp])
		#print os.path.join(sites, removeSite)
		shutil.rmtree(os.path.join(sites, removeSite))
		
def listSpam(sites):
	for site in os.listdir(sites):
		number = len([f for f in os.listdir(os.path.join(sites, site)) if os.path.isfile(os.path.join(sites, site, f))])
		if number < 10 or number > 30:
			print site
	
def changeHtml(sites):
	for site in os.listdir(sites):
		for file in os.listdir(os.path.join(sites, site)):
			if file.endswith('.html'):
				try:
					with open(os.path.join(sites, site, file)) as f:
						content = f.read()
					if " with " in content:
						content = content.replace(" with "," ",1)
					elif " some " in content:
						content = content.replace(" some "," ",1)
					elif " and " in content:
						content = content.replace(" and "," ",1)
					elif " is " in content:
						content = content.replace(" is "," ",1)
	 				with open(os.path.join(sites, site, file),'w') as f:
	 					f.write(content)
 				except:
 				 	print site
		try:
			for file in os.listdir(os.path.join(sites, site, 'config')):
				if file.endswith('.html'):
					with open(os.path.join(sites, site, 'config', file)) as f:
						content = f.read()
					if " with " in content:
						content = content.replace(" with "," ",1)
					elif " some " in content:
						content = content.replace(" some "," ",1)
					elif " and " in content:
						content = content.replace(" and "," ",1)
					elif " is " in content:
						content = content.replace(" is "," ",1)
 					with open(os.path.join(sites, site, 'config',file),'w') as f:
 						f.write(content)
		except:
			pass

def removeSites(allFile,saveFile):
	with open(allFile) as f:
		all = [line.strip()for line in f]
	with open(saveFile) as f:
		save = [line.strip() for line in f]
	
	remove = list(set(all)-set(save))
	with open('C:/Users/revotu/Desktop/task_seo/remove-dir.txt','w') as f:
		for line in remove:
			f.write(line + '\n')
		
def listDIR(sites):
	for site in os.listdir(sites):
		print site

def removeHistorySpamFiles(sites):
	for site in os.listdir(sites):
		root = os.path.join(sites, site, 'public_html')
		if not os.path.exists(root):
			root = os.path.join(sites, site)
		with open(os.path.join(root, 'index.php')) as f:
			content = f.read()
			saveFiles = re.findall(r'file_get_contents\(\'(.+?)\'\)', content)
			saveFiles = [os.path.join(root, saveFile).replace('.///','').replace('.//','').replace('\\','/') for saveFile in saveFiles ]

			saveFiles.extend([os.path.join(root, 'config', 'index_template.html').replace('\\','/'),os.path.join(root, 'config', 'template.html').replace('\\','/')])

		for cur, dirnames, filenames in os.walk(root):
			for filename in filenames:
				if filename.endswith('.txt'):
					if filename not in ['today.txt','sitemap.txt']:
						os.remove(os.path.join(cur, filename))
				if filename.endswith(('.swp', '_removed', '.bak')) or filename == 'log':
					os.remove(os.path.join(cur, filename))
				if filename.endswith('.htmlremoved'):
					shutil.move(os.path.join(cur, filename), os.path.join(cur, filename.replace('.htmlremoved','.html')))
					filename = filename.replace('.htmlremoved','.html')
				if filename.endswith('.html'):
					if os.path.join(cur, filename).replace('\\','/') not in saveFiles:
						if os.path.join(cur, filename + '.html').replace('\\','/') in saveFiles:
							shutil.move(os.path.join(cur, filename), os.path.join(cur, filename + '.html'))
						else:
							os.remove(os.path.join(cur, filename))

		for filename in os.listdir(os.path.join(root, 'config')):
			if not filename.endswith('.html'):
				os.remove(os.path.join(root, 'config', filename))

		matches = ['1']
		while matches:
			matches = []
			for cur, dirnames, filenames in os.walk(root):
				for dirname in dirnames:
					try:
						os.rmdir(os.path.join(cur, dirname))
						matches.append(os.path.join(cur, dirname))
					except:
						pass
		print site

def replaceHistoryDomains(sites, replaceFile):
	with open(replaceFile) as f:
		rewriteRules = {}
		for line in f:
			src, dst = line.strip().split('`')
			rewriteRules[src] = dst

	for site in os.listdir(sites):
		src = site.replace('www.','')
		if src in rewriteRules:
			dst = rewriteRules[src]
			replaceSite = site.replace(src, dst)
			replaceSitePath = os.path.join(sites,replaceSite)
			os.rename(os.path.join(sites,site),replaceSitePath)

			for root, dirnames, filenames in os.walk(replaceSitePath):
				for filename in filenames:
					if filename.endswith(('.txt', '.html', '.php')):
						replaceDomain(os.path.join(root, filename), src, dst)
						if src in filename:
							os.rename(os.path.join(root, filename), os.path.join(root, filename.replace(src, dst)))
						if src.split('.')[0] in filename:
							os.rename(os.path.join(root, filename), os.path.join(root, filename.replace(src.split('.')[0], dst.split('.')[0])))

		print site

def main():
# 	sites = 'C:/Users/revotu/Desktop/task_seo/sites-all/'
 	replaceFile = 'E:\\task\\rules\\replace-domain.csv'
# 	config(sites, replaceFile)
# 	sites = 'C:/Users/revotu/Desktop/task_seo/sites-all/'
# 	extractLogo(sites)
# 	sites = 'C:/Users/revotu/Desktop/task_seo/sites-all'
# 	phpSite = 'C:/Users/revotu/Desktop/task_seo/php-sites.txt'
# 	removePHP(sites, phpSite, replaceFile)
# 	sites = 'C:/Users/revotu/Desktop/task_seo/sites-all'
# 	changeHtml(sites)
# 	allFile = 'C:/Users/revotu/Desktop/task_seo/all-dir.txt'
# 	saveFile = 'C:/Users/revotu/Desktop/task_seo/good_domain.csv'
# 	removeSites(allFile,saveFile)
# 	sites = 'C:/Users/revotu/Desktop/task_seo/sites-all'
# 	listDIR(sites)

 	sites = 'E:/task/data'
	#replaceHistoryDomains(sites, replaceFile)
	#removeHistorySpamFiles(sites)
	
	# sites = 'C:/Users/revotu/Desktop/task_seo/sites'
	logos = 'E:\\task\\logos'
	# replaceFile = 'C:/Users/revotu/Desktop/task_seo/replace-domain.csv'
	replaceLogo(sites, logos, replaceFile)

if __name__ == "__main__":
	main()