import pywikibot
from pywikibot import pagegenerators
from pywikibot.data import api
import numpy as np
import requests
import mwparserfromhell
import re


site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
enwiki = pywikibot.Site('en', 'wikipedia')
enwiki_repo = enwiki.data_repository()
targetcat = 'Category:Amazon_author_page_not_in_Wikidata'
cat = pywikibot.Category(enwiki, targetcat)
subcats = pagegenerators.SubCategoriesPageGenerator(cat, recurse=False);
# for subcat in subcats:
    # print (subcat.title(), 'done')



pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False);
d = {}
      
count = 0  
book_id_list = []  
for page in pages:
    y = page.title()
    text = page.get()
    #print(text)
    ext = text.split('==External links==')[1].split('{{Authority control}}')[0].strip()
    #print(text)
    ext1 = ext.split('\n')
    #print (ext1)
    for item in ext1 :
        z = re.search(r'(?:\| [a-zA-Z].*\S [a-z A-Z].* \S) ', item)
        x = re.search(r'\w[a-zA-Z].* \S{1} ', item)
        
        if z is not None:
            id_item = z.group().split('|')[1].split('=')[1].strip()
            book_id_list.append(id_item)     # creats a list of book IDs
            
        # if count > 1:
            # print('this id exits on more than one page')
            # break            
        if x is not None:
            id_item1 = x.group().split('|')
            prop = id_item1[0].strip()
            #amazon_id = id_item[1].strip()
            label = 'Amazon author page'
            d[prop] =  id_item
            if prop.casefold() == label.casefold():
                page_wiki = pywikibot.Page(enwiki, y)
                item_from_wiki = str (pywikibot.ItemPage.fromPage(page_wiki))
                qid_for_page = item_from_wiki.split('[[')[1].split(']]')[0].split(':')[1]
                print(qid_for_page)
                item1 = pywikibot.ItemPage(repo, qid_for_page)
                url = 'https://www.amazon.com/wd/e/' + id_item
                print(url)
                Identifiersclaim = pywikibot.Claim(repo, u'P4862')
                Identifiersclaim.setTarget(id_item)   
                item1.addClaim(Identifiersclaim, summary=u'Adding Amazon Author ID') 
                print(done)                
            

            
  
  
for ids in book_id_list:
    sparql = "SELECT ?item ?amazon_author_id WHERE { ?item wdt:P4862 ?amazon_author_id filter(?amazon_author_id =" + '"'+ id_item +'"' + " )} "
    generator = pagegenerators.WikidataSPARQLPageGenerator(sparql, site=enwiki_repo)
    for page in generator:
        count = count+1
    if count >1 :
      print ( 'more than one page use this amazon author id :' , ids)     