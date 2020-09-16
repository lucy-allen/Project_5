#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:36:27 2020

@author: lucyallen
"""


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
from math import cos, asin, sqrt, pi

resorts = pd.read_csv('Resorts_Clean.csv')
resorts.drop('Unnamed: 0', axis=1, inplace=True)
scaler = StandardScaler()

resorts_less = resorts.copy()
resorts_less.drop(['Resort_Name', 'Region', 'State', 'Longditude', 'Latitude', 'Base_Elevation', 'Intermediate_Distance', 'Pct_Intermediate'], axis=1, inplace=True)
scaled_resorts_less = scaler.fit_transform(resorts_less)
scaled_resorts_df = pd.DataFrame(scaled_resorts_less)


def scale_resorts_data(df):
    df_less = df.drop(['Resort_Name', 'Region', 'State', 'Longditude', 'Latitude', 'Base_Elevation', 'Intermediate_Distance', 'Pct_Intermediate'], axis=1)
    scaled_df = scaler.transform(df_less)
    return pd.DataFrame(scaled_df)

def limit_region(df, region):
    new_df = df[df['Region'] == region].reset_index()
    new_df.drop('index', axis=1, inplace=True)
    return new_df

def limit_price(df, price):
    new_df = df[df['Price'] <= price].reset_index()
    new_df.drop('index', axis=1, inplace=True)
    return new_df

def limit_distance(df, dist, lat, lon):
    new_df = df.copy()
    new_df['distance_mi'] = distance(new_df['Latitude'], new_df['Longditude'], lat, lon)
    new_df = new_df[new_df['distance_mi'] <= dist].reset_index()
    new_df.drop('index', axis=1, inplace=True)
    return new_df

def limit_beginner(df):
    new_df = df[df['Pct_Easy'] > 40].reset_index()
    new_df.drop('index', axis=1, inplace=True)
    return new_df

def find_closest(name, index, num, scaled_df, df_with_names):
    '''Finds the closest episode, using Cosine Distances to the
    episode of interest
    Inputs: Index of Episode of Interest, Number of closest episodes to return
    Returns: list of indexes of closest episodes'''
    ordered_array = pairwise_distances(np.array(scaled_resorts_df.loc[index]).reshape(1, -1)
                                       ,scaled_df,metric='euclidean').argsort()
    #print(ordered_array)
    #print(index)
    #print(ordered_array[0][0:7])
    scaled_idx = name_to_index(name, df_with_names)
    #print(scaled_idx)
    top = []
    if ordered_array[0][0] == scaled_idx:
        for i in range(1, num+1):
            top.append(ordered_array[0][i])
        return top
    else:
        for i in range(0, num):
            top.append(ordered_array[0][i])
        return top


def name_to_index(resort, df):
    try:
        idx = df[df['Resort_Name'] == resort].index[0]
    except IndexError:
        idx = 262
    return idx

def find_resort(resort, num, df):
    '''Finds the titles associated with the closest 
    Uses find_closest, so the inputs can be the same, 
    but instead returns titles not indexes so it is more user friendly'''
    
    try:
        scaled_df = scale_resorts_data(df)
    except ValueError:
        return 'No resorts With these specifications!'
    index = name_to_index(resort, resorts)
    try:
        idx = find_closest(resort, index, num, scaled_df, df)
    except KeyError:
        return 'No resort with that name! Please try again!'
    resort_list = []
    for i in idx:
        resort_list.append(df.loc[i, 'Resort_Name'])
    return resort_list


def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
    km = 12742 * np.arcsin(np.sqrt(a))
    return km*0.621371

print(find_resort('Breckenridge', 5, resorts))

#resorts_data = limit_price(resorts, 200)
#print(find_resort('Vail', 5, resorts_data))

#print(limit_distance(resorts, 300, 41.6651, -70.0892))

vail = resorts[resorts['Resort_Name']=='Vail']
big_sky = resorts[resorts['Resort_Name']=='Big Sky Resort']
breckenridge = resorts[resorts['Resort_Name']=='Breckenridge']
killington = resorts[resorts['Resort_Name'] == 'Killington']
snowmass = resorts[resorts['Resort_Name'] == 'Snowmass']
jackson_hole = resorts[resorts['Resort_Name'] == 'Jackson Hole']
sugarbush = resorts[resorts['Resort_Name'] == 'Sugarbush']
telluride = resorts[resorts['Resort_Name'] == 'Telluride']
snowbasin = resorts[resorts['Resort_Name'] == 'Snowbasin']
winter_park = resorts[resorts['Resort_Name'] == 'Winter Park Resort']

#print(find_resort('Vail'))
#print(name_to_index('Vail'))
#print(name_to_index('Sun Valley'))
#print(find_resort('Sun Valley'))
#print(resorts[resorts['Resort_Name'] == 'Sun Valley'])
#print(limit_region(resorts, 'Eastern US').head())
vail_scale = scale_resorts_data(vail)
big_sky_scale = scale_resorts_data(big_sky)
killington_scale = scale_resorts_data(killington)
snowmass_scale = scale_resorts_data(snowmass)
breckenridge_scale = scale_resorts_data(breckenridge)
sugarbush_scale = scale_resorts_data(sugarbush)
jackson_hole_scale = scale_resorts_data(jackson_hole)
telluride_scale = scale_resorts_data(telluride)
winter_park_scale = scale_resorts_data(winter_park)

print(pairwise_distances(np.array(vail_scale).reshape(1, -1)
                                     ,killington_scale,metric='euclidean'))







