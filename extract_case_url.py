import os
import re
import urllib2

def extract_case_url(url,caseSite):
    print url,caseSite
    
    html = urllib2.urlopen(url).read()
    
    luman_reg = re.compile(r'"lumen_url":"(.+?)"')
    data = luman_reg.findall(html)
    
    dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dir,'%s-case-url' % (caseSite))
    
    if len(data) > 0:
        luman_url = data[0]
        luman_html = urllib2.urlopen(luman_url).read()
        
        site_reg = re.compile(r'http.+?html')
        site_data = site_reg.findall(luman_html)
        for site in site_data:
            if caseSite in site:
                print "%s\t\t%s"  % (luman_url,site)
                with open(filename,"a") as f:
                    f.write("%s\t\t%s\n"  % (luman_url,site))


if __name__ == "__main__":
    caseSite = 'sausalitostory.com'
    
    caseList = ['3033167','3033692','3031585','3019400','3021402','3016287','3014586','3016000','3016831','3016864','3012703','3013509','3011387','3013565','3011024','3011308','3011566','3011941','3013910','3010013','3010647','3012575','3010428','3013724','3011717','3013347','3012182','3013226','3011359','3010935','3010964','3011121','3011064','3011472','3011158','3012671','3010334','3011898','3012373','3012943','3010477','3010064','3013079']
    
    for case in caseList:
        url = 'https://www.google.com/transparencyreport/api/v2/reports/copyright/products/search/requests/%s/?alt=JSONP&c=angular.callbacks._0' % case
        extract_case_url(url,caseSite)