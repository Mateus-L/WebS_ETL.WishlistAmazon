#!/usr/bin/env python
# coding: utf-8

# In[3]:


from selenium import webdriver
import time
import pandas as pd

precos = []
produtos = []
c= 0

#driver
driver = webdriver.Chrome(executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
driver.get('https://www.amazon.com.br/hz/wishlist/ls/39H1LPR1DWM0K/ref=nav_wishlist_lists_2?_encoding=UTF8&type=wishlist&viewType=grid')
time.sleep(1.5)
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div/div[2]/div[4]/div/div/div/div/div[1]/span[2]/a/div[1]/span'
                            ).click()
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/div/div/ul/li/span/span/a').click()
time.sleep(1.5)


#nome dos produtos e contagem
for x in range (150):
    try:
        n = driver.find_element_by_xpath(f'/html/body/div[1]/div/table/tbody/tr[{x+2}]/td[2]/span[1]').text
        produtos.append(n)
        c+=1
    except:
        next

#preços e correção de null

for x in range (2,c+2,1):
    try:
        p = driver.find_element_by_xpath(f'/html/body/div[1]/div/table/tbody/tr[{x}]/td[4]/span').text
        precos.append(p)
    except:
        precos.append('R$ 00,00')
        next
        
driver.close()


# In[4]:


#criando DF, corrigindo valores e calculando total

data = {'Produto':produtos,'Preço':precos}
df = pd.DataFrame(data)
df["Preço"] = df["Preço"].replace('[\$\"R"\.]',"",regex=True)
df["Preço"] = df["Preço"].replace('[\,]',".",regex=True).astype('float')

print(f'Quantidade total de produtos: {df["Produto"].count()}')
print(f'Valor total da lista: {sum(df["Preço"])}')

df.sort_values('Preço',ascending=False)
