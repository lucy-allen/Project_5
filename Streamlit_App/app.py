#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 15:16:47 2020

@author: lucyallen
"""


import streamlit as st
import pandas as pd
import numpy as np
import pickle
from Function import find_resort, limit_region, limit_price, limit_distance, name_to_index, limit_beginner

resorts_df = pd.read_csv('Resorts_Clean.csv')
resorts_df.drop('Unnamed: 0', axis=1, inplace=True)

st.title('Ski Resort Recommender')
st.image('Jan2016_small.jpg', width=700)
st.markdown("---")
st.subheader("Share your favorite Ski Resort and I will recommend you a new one, that I know you'll like!")


no_fave = st.selectbox('Do You Have a Favorite Resort?', ['Yes', 'No'])
'You selected:', no_fave

  
region = st.selectbox('Do you have a region of preference', ['ALL', 'Western US', 'Eastern US', 'Midwest US'])
'You selected: ', region

#coords = resorts_df[['Latitude', 'Longditude']]
#coords.rename(columns={'Latitude':'lat', 'Longditude':'lon'}, inplace=True)
#st.map(coords)
#no_prev_fave = st.checkbox('I do not have a favorite resort:(')

if no_fave == 'Yes':    
    fave_resort = st.selectbox('Which Ski Resort do you like best?', resorts_df['Resort_Name'])
    'You selected: ', fave_resort
    
if no_fave == 'No':
    beginner = st.selectbox('Are you a beginner?', ['Yes', 'No'])

price_limit = st.checkbox('I have a maximum price I am willing to spend on a lift ticket')
if price_limit == True:
    price_max = st.selectbox('What is your maximum price?', [200, 180,  160,  140, 120, 100, 80, 60, 40, 30, 20])
else:
    price_max = 250

location = st.checkbox('I would like to consider proximity to my location')
if location == True:
    longditude = st.number_input('Please Enter your Longditude')
    latitude = st.number_input('Please Enter your Latitude')
    max_dist = st.number_input('Enter the maximum distance you would like to go (in mi)')
    
    
num_recs = st.selectbox('How many recommendations would you like to see?', range(1,11))
'You want to see: ', str(num_recs), ' recommendations'


resorts_df = limit_price(resorts_df, price_max)

if location == True:
    resorts_df = limit_distance(resorts_df, max_dist, latitude, longditude)
    resorts_df.drop('distance_mi', axis=1, inplace=True)

if region != 'ALL':
    resorts_df = limit_region(resorts_df, region)

coords = resorts_df[['Latitude', 'Longditude']]
coords.rename(columns={'Latitude':'lat', 'Longditude':'lon'}, inplace=True) 
    
    
    
if no_fave == 'Yes':
    if st.button('Recommend Me Some Resorts'):
        try:
            recommendations = find_resort(fave_resort, num_recs, resorts_df)
            if len(recommendations) == num_recs:
                index_vals = []
                for rec in recommendations:
                    index_vals.append(name_to_index(rec, resorts_df))
                for idx, rec in enumerate(recommendations):
                    st.write(str(idx+1) + '. ', rec)
                st.map(coords.iloc[index_vals])
                st.write('Happy Skiing!!')
            else:
                st.write(''.join(recommendations))
        except IndexError:
            for i in range(1, num_recs):
                try:
                    recommendations = find_resort(fave_resort, num_recs-i, resorts_df)
                    for idx, rec in enumerate(recommendations):
                        st.write(str(idx+1) + '. ', rec)
                    break
                except IndexError:
                    st.write('')
                    #st.write('No Resorts with those Requirements!')
            st.write('Could Not Find Any More Matches')
            st.write('Happy Skiing!!')
else:
    if st.button('Recommend Me Some Resorts'):
        if beginner == 'No':
            recommendations = []
            for i in range(num_recs):
                recommendations.append(resorts_df.loc[i, 'Resort_Name'])
            index_vals = []
            for rec in recommendations:
                index_vals.append(name_to_index(rec, resorts_df))
            for idx, rec in enumerate(recommendations):
                st.write(str(idx+1) + '. ', rec)   
            st.map(coords.iloc[index_vals])
        else:
            resorts_beg = limit_beginner(resorts_df)
            recommendations = []
            for i in range(num_recs):
                recommendations.append(resorts_beg.loc[i, 'Resort_Name'])
            index_vals = []
            for rec in recommendations:
                index_vals.append(name_to_index(rec, resorts_df))
            for idx, rec in enumerate(recommendations):
                st.write(str(idx+1) + '. ', rec)            
            st.map(coords.iloc[index_vals])
        

    st.write('Happy Skiing!!')

#coords = resorts_df[['Latitude', 'Longditude']]
#coords.rename(columns={'Latitude':'lat', 'Longditude':'lon'}, inplace=True)
#index_vals = []
#for rec in recommendations:
 #   index_vals.append(name_to_index(rec, resorts_df))
   
#coords.iloc[index_vals]  
#coords = resorts_df[['Latitude', 'Longditude']]
#coords.rename(columns={'Latitude':'lat', 'Longditude':'lon'}, inplace=True)
#st.map(coords.iloc[index_vals])
#if location == True or region != 'ALL':
 #   st.map(coords)
st.image('Whitefish.JPG', width=700)
st.write('Data Source: skiresort.info')
#print(resorts.head(5))




