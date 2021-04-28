import pywikibot
from pywikibot import pagegenerators
from pywikibot.data import api
import numpy as np
import requests
import mwparserfromhell
import re




enwiki = pywikibot.Site('en', 'wikipedia')
enwiki_repo = enwiki.data_repository()
targetcat = 'Category:Amazon_author_page_not_in_Wikidata'
cat = pywikibot.Category(enwiki, targetcat)
subcats = pagegenerators.SubCategoriesPageGenerator(cat, recurse=False);
for subcat in subcats:
    print (subcat.title(), 'done')


site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()


pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False);
d = {}
    
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
            #print(id_item)   #reutrns ID on external link.
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

            
  
  
  