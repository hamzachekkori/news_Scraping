import requests
from bs4 import BeautifulSoup
import numpy as np
import time
#j'importe pymongo pour utuliser MangoDb 
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#je nomme et je crée ma base de donnée
mydb = myclient["UniteRemote"]
mycol = mydb["CodeChallenge"]





# url affectation
url = "https://www.bbc.com/"

# Les Request
r1 = requests.get(url)
r1.status_code

# We'll save in coverpage the cover page content
#je vais enregistrer dans la PagedeCouverture le contenue html de notre site web
coverpage = r1.content

# Création de ma premiere soup
soup1 = BeautifulSoup(coverpage, 'html5lib')

#  Identification des News 
#  Je vais les identifier en cherchant leurs titres
# puis je vais compter combien de titre j'ai dans ma page ce qui me donne le nombre de news dans ma page

coverpage_news = soup1.find_all('h3', class_='media__title')
len(coverpage_news)

# Nous avons maintenant une liste dans laquelle chaque élément est une news mais contient encore des balises HTML qu'on on l'extrait

coverpage_news[4]

#Extrayons le texte des news:
#on fait le test sur les 5 premiers articles

number_of_articles = 5

# Empty lists for content, links and titles
# je declare 3 listes 1 pour les titres,1 pour content,1 pour les liens

news_contents = []
list_links = []
list_titles = []

for n in np.arange(0, number_of_articles):

# jusqu'a present chaque coverpage_news[n] contient une balise <a> --> le lien  et le titre qui est text 
#    1.1) extrayons le lien d'une news
#    1.2) ajoutons le a la liste des liens    
    link = coverpage_news[n].find('a')['href']
    list_links.append(link)       
    
#    2.1) extrayons le titre d'une news
#    2.2) ajoutons le a la liste des titres
    title = coverpage_news[n].find('a').get_text()
    list_titles.append(title)  

# lire le contenue des news les contenue des liens (et ils sont divisé en paragraphe) 
# je vais construire l'url complet et l'ajouter a l'URL avec le href des nouvelles news
    article = requests.get("https://www.bbc.com/"+link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
#chaque bloc de news contient le titre le lien et la description du news qui se trouve dans chaque div et sa class= 'story-body'   
    body = soup_article.find_all('div', class_='story-body')
    x = body[0].find_all('p')
# je vais rassembler les paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
        
    news_contents.append(final_article)   

# je vais envoyer les titres et les liens que j'ai collecté a la base donnée MongoDb     
# je vais charger la 1ere liste par les titres et les liens
mylist=[
{'Article Title': list_titles,
 'Article Link': list_links}]   
# je vais charger la 2eme liste avec le contenue des news
mylist2=[{'Article Content': news_contents }]

#j'insere dans MangoDb a l'aide de insert_many
xx = mycol.insert_many(mylist)
xxx = mycol.insert_many(mylist2)    
    
#j'ai importer la bibliotheque time 
#pour calculer Temps que passe le script pour obtenir les resultas
#et Pour cela je vais mettre tous ce qui précede dans une fonction 
    
#def Recolte_News_Bbc():
#            # url affectation
#        url = "https://www.bbc.com/"
#        
#        # Les Request
#        r1 = requests.get(url)
#        r1.status_code
#        
#        # We'll save in coverpage the cover page content
#        #je vais enregistrer dans la PagedeCouverture le contenue html de notre site web
#        coverpage = r1.content
#        
#        # Création de ma premiere soup
#        soup1 = BeautifulSoup(coverpage, 'html5lib')
#        
#        #  Identification des News 
#        #  Je vais les identifier en cherchant leurs titres
#        # puis je vais compter combien de titre j'ai dans ma page ce qui me donne le nombre de news dans ma page
#        
#        coverpage_news = soup1.find_all('h3', class_='media__title')
#        len(coverpage_news)
#        
#        # Nous avons maintenant une liste dans laquelle chaque élément est une news mais contient encore des balises HTML qu'on on l'extrait
#        
#        coverpage_news[4]
#        
#        #Extrayons le texte des news:
#        #on fait le test sur les 5 premiers articles
#        
#        number_of_articles = 5
#        
#        # Empty lists for content, links and titles
#        # je declare 3 listes 1 pour les titres,1 pour content,1 pour les liens
#        
#        news_contents = []
#        list_links = []
#        list_titles = []
#        
#        for n in np.arange(0, number_of_articles):
#        
#        # jusqu'a present chaque coverpage_news[n] contient une balise <a> --> le lien  et le titre qui est text 
#        #    1.1) extrayons le lien d'une news
#        #    1.2) ajoutons le a la liste des liens    
#            link = coverpage_news[n].find('a')['href']
#            list_links.append(link)       
#            
#        #    2.1) extrayons le titre d'une news
#        #    2.2) ajoutons le a la liste des titres
#            title = coverpage_news[n].find('a').get_text()
#            list_titles.append(title)  
#        
#        # lire le contenue des news les contenue des liens (et ils sont divisé en paragraphe) 
#        # je vais construire l'url complet et l'ajouter a l'URL avec le href des nouvelles news
#            article = requests.get("https://www.bbc.com/"+link)
#            article_content = article.content
#            soup_article = BeautifulSoup(article_content, 'html5lib')
#        #chaque bloc de news contient le titre le lien et la description du news qui se trouve dans chaque div et sa class= 'story-body'   
#            body = soup_article.find_all('div', class_='story-body')
#            x = body[0].find_all('p')
#        # je vais rassembler les paragraphs
#            list_paragraphs = []
#            for p in np.arange(0, len(x)):
#                paragraph = x[p].get_text()
#                list_paragraphs.append(paragraph)
#                final_article = " ".join(list_paragraphs)
#                
#            news_contents.append(final_article)   
#        
#        # je vais envoyer les titres et les liens que j'ai collecté a la base donnée MongoDb     
#        # je vais charger la 1ere liste par les titres et les liens
#        mylist=[
#        {'Article Title': list_titles,
#         'Article Link': list_links}]   
#        # je vais charger la 2eme liste avec le contenue des news
#        mylist2=[{'Article Content': news_contents }]
#        
#        #j'insere dans MangoDb a l'aide de insert_many
#        xx = mycol.insert_many(mylist)
#        xxx = mycol.insert_many(mylist2)    
#

#Pour tester la Rapidité de mon programme
#Debut = time.time()
#Recolte_News_Bbc()
#Fin =time.time()
#Temp_Ecoule = Fin-Debut
#print("Le Temp passé est  %f seconds" %(Temp_Ecoule))            
#        
    
    
    
    
    

