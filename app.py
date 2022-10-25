# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 18:52:35 2022

@author: MAYUR
"""

import pandas as pd
pd.set_option('display.max_columns', None)
import requests
from bs4 import BeautifulSoup


import warnings
warnings.filterwarnings('ignore')

import streamlit as st

st.set_page_config(page_title='BBC News Scrapper', page_icon='newspaper.png', layout="wide", initial_sidebar_state="auto", menu_items=None)

#####################################################

embed_component = {'Linkedin': """<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
               <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="Dark" data-type="HORIZONTAL" data-vanity="mayur-shrotriya" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://www.linkedin.com/in/mayur-shrotriya-b45133142?trk=profile-badge">Connect with me!</a></div>
               """ }
              
               
import streamlit.components.v1 as components
with st.sidebar:
    components.html(embed_component['Linkedin'], height=500)


###################################################### Aesthetics ######################################################################
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)

############################################################ Title
c1 , c2, c3 , c4= st.columns([1,1,2,2])
c3.markdown("<h1 style='text-align: center;'><font face='High Tower Text'> BBC News Scrapper </font></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: right; color: #ffd11a;'><font face='Brush Script MT' weight=5 size=5>-By Mayur Shrotriya</font></p>", unsafe_allow_html=True)

st.markdown("***")
st.write()


############################################################ Inputs


search_word = 'tony stewart nft'

c1,c2,c3,c4,c5,c6 = st.columns([1,2,1,2,1,1])

c1.write(" ")
c1.write(" ")
c1.write(" ")

c1.markdown("""
           <p style='text-align: right;'> I want to search for :</p>
           """, unsafe_allow_html=True)
search_word = c2.text_input('Type your search words here :')

c4.write(" ")
c4.write(" ")
c4.write(" ")
c4.markdown("""
           <p style='text-align: right;'> Number of results I want is </p>
           """, unsafe_allow_html=True)
no_of_results = c5.number_input('No. of results:', min_value=10, step = 10)# 20 # Multiples of 10

if search_word != '':
    
    st.markdown('***', unsafe_allow_html=True )

    no_of_pages = no_of_results // 10 + 1
    
    search_word = search_word.replace(" ",r'+')
    
    # Collection of links
    headlines = []
    subheadings = []
    links = []
    articles = []
    
    
    
    # Getting data from main pages.
    for i in range(1,no_of_pages):
        url='https://www.bbc.co.uk/search?q=' + search_word + '&page='+str(i)
        # Requesting data
        response = requests.get(url)
        
        # Getting the data into soup
        soup = BeautifulSoup(response.text, 'html5lib')
        
        # Getting links
        links_ = soup.find_all('a', class_='ssrcss-1ynlzyd-PromoLink e1f5wbog0') #getting link text of 1 page
        for j in links_:
            links.append(j.get('href'))
        
        # Getting headlines
        heads = soup.find_all('p', class_='ssrcss-6arcww-PromoHeadline e1f5wbog4')
        for k in heads:
            headlines.append(k.get_text())
        
        # Getting the Sub headings
        subheads = soup.find_all('p', class_='ssrcss-1q0x1qg-Paragraph eq5iqo00')[:10]
        for l in subheads:
            subheadings.append(l.get_text())
        
        
        
    # progress = st.progress(0)
    # count = 100//len(links)
    # x = 0
    # Getting Articles
    with st.spinner('Please wait!'):
        for url in links:
            response = requests.get(url)
            sub_soup = BeautifulSoup(response.text, 'html5lib')
            article = ''
            for i in sub_soup.find_all('p', class_='ssrcss-1q0x1qg-Paragraph eq5iqo00')[1:-1]:
                article += i.get_text() + ' '
            if article == '':
                for i in sub_soup.find_all('p', class_=''):
                    article += i.get_text() + ' '
        
            # print(article + "_")
            articles.append(article)
            
            # x += count
            
            # progress.progress(x)
        
    # Making Data Frame
    df = pd.DataFrame(columns=['Link','Headline', 'Intro_Paragraph', 'Article'])
    df['Link'] = links
    df['Headline'] = headlines
    df['Intro_Paragraph'] = subheadings
    df['Article'] = articles
    
    
    st.table(df.head())

    st.download_button('Download the Dataframe', df.to_csv() , 'BBC News' + search_word + '.csv')




























