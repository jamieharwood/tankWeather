#!/usr/bin/env python3

import requests
import psycopg2

def main():
    
    resp = requests.get('http://api.wunderground.com/api/29c8c14c8a1fabe6/conditions/q/CA/whitstable.json')

    if resp.status_code != 200:
	        raise ApiError('GET /tasks/ {}'.format(resp.status_code))

    else:
        retrieved = resp.json()

        conn = psycopg2.connect(host='localhost', dbname='tankstore', user='tank', password='skinner2')
        conn.autocommit = True
        cur = conn.cursor()

        sql = "INSERT INTO public.weather (weather, temp_c, wind_dir, wind_mph, wind_gust_mph, windchill_c, feelslike_c, visibility_mi) VALUES ('{0}', {1},'{2}', {3}, {4}, {5}, {6}, {7})"
        sql = sql.replace('{0}', retrieved['current_observation']['weather'])
        sql = sql.replace('{1}', str(retrieved['current_observation']['temp_c']))
        sql = sql.replace('{2}', retrieved['current_observation']['wind_dir'])
        sql = sql.replace('{3}', str(retrieved['current_observation']['wind_mph']))
        sql = sql.replace('{4}', str(retrieved['current_observation']['wind_gust_mph']))
        sql = sql.replace('{5}', str(retrieved['current_observation']['windchill_c']))
        sql = sql.replace('{6}', str(retrieved['current_observation']['feelslike_c']))
        
        if (str(retrieved['current_observation']['visibility_mi']) == "N/A"):
            sql = sql.replace('{7}', "-1")
        else:
            sql = sql.replace('{7}', str(retrieved['current_observation']['visibility_mi']))
        
        cur.execute(sql)

main()
