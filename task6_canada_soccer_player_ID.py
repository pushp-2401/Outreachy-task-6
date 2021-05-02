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


targetcat = 'Category:Canada_Soccer_player_ID_not_in_Wikidata'
cat = pywikibot.Category(enwiki, targetcat)
subcats = pagegenerators.SubCategoriesPageGenerator(cat, recurse=False);
for subcat in subcats:
    print (subcat.title(), 'done')



pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False);
id_list = []  
for page in pages:
    y = page.title()
    text = page.get()
    x = re.search("Canada Soccer player\S([0-9]*)", text)    #<re.Match object; span=(8611, 8636), match='Canada Soccer player|4720'>
    if x is not None :
        x1 = x.group()          #Canada Soccer player|4720
        player_id = x1.split('|')[1].strip()
        id_list.append(player_id)
        #print(player_id)
        check = player_id.isnumeric()
        if check:
            page_wiki = pywikibot.Page(enwiki, y)
            item_from_wiki = str (pywikibot.ItemPage.fromPage(page_wiki))
            qid_for_page = item_from_wiki.split('[[')[1].split(']]')[0].split(':')[1]
            item1 = pywikibot.ItemPage(repo, qid_for_page)
            Identifiersclaim = pywikibot.Claim(repo, u'P7459')
            Identifiersclaim.setTarget(player_id)   
            item1.addClaim(Identifiersclaim, summary=u'Adding canada soccer player id') 
            print('done') 
                        
        
print(id_list) 
       
for id_number in id_list:
    properties = 'P7459'
    sparql = 'SELECT ?item WHERE { ?item wdt:'+properties+' ?id . FILTER (?id = "'+id_number+'") . }'
    generator = pagegenerators.WikidataSPARQLPageGenerator(sparql, site=enwiki_repo)
    count = 0
    page_list = []
    for page in generator: 
        count = count+1
        page_list.append(page)
    if count > 1 :
      print ( 'more than one page use this Canada soccer player ID: ' , id_number,',', page_list)