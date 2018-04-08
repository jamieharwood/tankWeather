#!/usr/bin/env python3

import psycopg2
from sensorStateClass import sensorState

def getRowCount(sql):
    conn = psycopg2.connect(host='localhost', dbname='tank', user='tank', password='skinner2')
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute(sql)
    rows = cur.fetchall()

    return len(rows)

def main():
    isWet = 0
    mySensorState = sensorState()
    
    sqlSnow = "select \"weatherTodayTypes\".weather as lweather from public.\"weatherTodayTypes\" WHERE lower(\"weatherTodayTypes\".weather) = 'snow';"
    sqlRain = "select \"weatherTodayTypes\".weather as lweather from public.\"weatherTodayTypes\" WHERE lower(\"weatherTodayTypes\".weather) = 'rain';"
    
    if getRowCount(sqlSnow) > 0 or getRowCount(sqlRain) > 0:
        isWet = 1

    mySensorState.setSensorID('10000001')
    mySensorState.setSensorType('weather-wet')
    mySensorState.setSensorValue(isWet)
    mySensorState.setSatus()

main()

