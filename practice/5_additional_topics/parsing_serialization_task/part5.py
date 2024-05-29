import json
import os
import sys
import xml.etree.cElementTree as ET
from xml.dom import minidom

rootdir = "/Users/broczniok/Desktop/PYTHON-BASIC/practice/5_additional_topics/parsing_serialization_task/source_data"
city_count = 0
mean_temp = 0
mean_wind_speed = 0
max_temp = -sys.maxsize - 1
warmest_place = ''
min_temp = sys.maxsize
coldest_place = ''
max_wind_speed = -sys.maxsize - 1
min_wind_speed = sys.maxsize

weather = ET.Element("weather", country="Spain", date="2021-09-25")
summary = ET.SubElement(weather, "summary")
cities = ET.SubElement(weather, "cities")

for subdir, dirs, files in os.walk(rootdir):
    current_place = os.path.basename(subdir)
    current_mean_temp = 0
    current_mean_wind_speed = 0
    current_min_temp = sys.maxsize
    current_max_temp = -sys.maxsize - 1
    current_min_wind_speed = sys.maxsize
    current_max_wind_speed = -sys.maxsize - 1

    for file in files:
        with open(os.path.join(subdir, file)) as f:
            data = json.load(f)
            hourly = data["hourly"]
            for hour in hourly:
                temp = int(hour["temp"])
                wind_speed = int(hour["wind_speed"])
                mean_temp += temp
                mean_wind_speed += wind_speed
                current_mean_temp += temp
                current_mean_wind_speed += wind_speed
                if max_temp < temp:
                    max_temp = temp
                    warmest_place = current_place
                if min_temp > temp:
                    min_temp = temp
                    coldest_place = current_place
                if max_wind_speed < wind_speed:
                    max_wind_speed = wind_speed
                if min_wind_speed > wind_speed:
                    min_wind_speed = wind_speed
                if current_max_temp < temp:
                    current_max_temp = temp
                if current_min_temp > temp:
                    current_min_temp = temp
                if current_max_wind_speed < wind_speed:
                    current_max_wind_speed = wind_speed
                if current_min_wind_speed > wind_speed:
                    current_min_wind_speed = wind_speed

    current_mean_temp = current_mean_temp / 24
    current_mean_wind_speed = current_mean_wind_speed / 24
    ET.SubElement(cities, 'city', name=current_place, mean_temp=str(current_mean_temp), mean_wind_speed=str(current_mean_wind_speed),
                  min_temp=str(current_min_temp), min_wind_speed=str(current_min_wind_speed), max_temp=str(current_max_temp),
                  max_wind_speed=str(current_max_wind_speed))
    city_count += 1

mean_temp = mean_temp / (city_count * 24)
mean_wind_speed = mean_wind_speed / (city_count * 24)
ET.SubElement(summary, "summary", mean_temp=str(mean_temp), mean_wind_speed=str(mean_wind_speed),
              coldest_place=coldest_place, warmest_place=warmest_place)

xml_str = ET.tostring(weather, encoding='utf-8', method='xml')

parsed_xml = minidom.parseString(xml_str)
pretty_xml_str = parsed_xml.toprettyxml(indent="  ")

with open("result.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml_str)
