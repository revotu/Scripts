# -*- coding:utf-8 -*-
import os
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def indexByDomain(domain):
	conn = MySQLdb.connect('45.79.71.23','mdtrade','trade@mingDA123','servers',charset="utf8")
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)

	cursor.execute('SELECT new_index FROM linksite WHERE site_name = "{}"'.format(domain))
	conn.commit()
	
	result = cursor.fetchall()

	cursor.close()
	conn.close()
	
	return result

def main():
	replaceFile = 'E:\\task\\rules\\replace-domain.csv'
	sites = 'E:\\task\\data'

	with open(replaceFile) as f:
		rewriteRules = {}
		for line in f:
			src, dst = line.strip().split('`')
			rewriteRules[dst] = src

	for site in os.listdir(sites):
		domain = site.replace('www.','')
		domain = rewriteRules[domain]
		result = indexByDomain(domain)
		index = result[0]['new_index']

		root = os.path.join(sites, site, 'public_html')
		if not os.path.exists(root):
			root = os.path.join(sites, site)
		try:
			with open(os.path.join(root, 'config', 'index_template.html')) as f:
				content = f.read()

			content = content.replace('###KEYWORD PLACE HOLDER###',index.replace('-',' ').replace('_',' '))
			content = content.replace('###CONTENT PLACE HOLDER###','')

			with open(os.path.join(root, index + '.html'), 'w') as f:
				f.write(content)

			print site,index+'.html'
		except:
			print 'error:',site

if __name__ == "__main__":
	main()