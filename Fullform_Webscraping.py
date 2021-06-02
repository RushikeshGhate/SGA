# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

url = 'https://fullforms.com/full-forms/R/6'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
table_data = soup.find('table', class_ = 'index-table')

letters = ['A','B']#,'C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


Popularity = []
Region=[]
Term=[]
Fullform=[]
MainCategory=[]
SubCategory=[]

for p in letters:
    number=0
    while True:
        page = requests.get(f'https://fullforms.com/full-forms/{p}/{number}')
        soup = BeautifulSoup(page.text, 'html.parser')
        count= soup.find_all('div', class_="pop-bar")
        #print(len(count),'_',p,'_',number)
        if len(count)==0:
            break
        #Popularity Column Values
       
        for pop in soup.find_all('div', class_="pop-bar"):
            Popularity.append(str(pop).split(':')[1].split(' ')[0].replace('%"','').strip())
            df_pop = pd.DataFrame(Popularity,columns=['Popularity'])
        #Country / Region Column Values 
        for region in soup.find_all('img',align=True):    
            Region.append(str(region).split(' ')[2].split('"')[1])
            df_reg=pd.DataFrame(Region,columns=['Region'])
        # Term Column Values
        for term in soup.find_all('td', class_="tT tblLink1"):
            Term.append(str(term).split(' ')[4])
            df_term = pd.DataFrame(Term,columns=['TERM'])
        # Full Form | Definition | Meaning column
        for heading in soup.find_all('td', class_="tD tblLink2"):
            Fullform.append(heading.text.strip())
            df_mean = pd.DataFrame(Fullform,columns=['Full Form | Definition | Meaning'])
        # MainCategory Column Values
        for mcat in soup.find_all('td', colspan="2" ,class_="tCat rowlink2"):
            MainCategory.append((mcat.text).split('»')[0].strip())
            df_mcat = pd.DataFrame(MainCategory,columns=['MainCategory'])
        #Sub Category Values
        for scat in soup.find_all('td', colspan="2" ,class_="tCat rowlink2"):
            SubCategory.append((scat.text).split('»')[1].strip())
            df_subcat = pd.DataFrame(SubCategory,columns=['SubCategory'])
        number+=1 
        df_new = pd.concat([df_pop,df_reg,df_term,df_mean,df_mcat,df_subcat],axis=1)
        df_new.to_csv('FullForm.csv')

print(len(df_pop),len(df_reg),len(df_term),len(df_mean),len(df_mcat),len(df_subcat))

