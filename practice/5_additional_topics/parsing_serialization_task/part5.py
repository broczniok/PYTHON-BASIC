import json
import os
import sys
import xml.etree.cElementTree as ET
from xml.dom import minidom


def sanitize_tag_name(tag_name):
    # Replace invalid characters with underscores
    return ''.join(c if c.isalnum() or c in '-_.' else '_' for c in tag_name)

rootdir = "source_data"
city_count = 0
mean_temp = 0
mean_wind_speed = 0
max_temp = -sys.maxsize - 1.0
warmest_place = ''
min_temp = float(sys.maxsize)
coldest_place = ''
max_wind_speed = -sys.maxsize - 1.0
min_wind_speed = float(sys.maxsize)
windiest_place = ''

weather = ET.Element("weather", country="Spain", date="2021-09-25")
summary = ET.SubElement(weather, 'summary')
cities = ET.SubElement(weather, "cities")

for subdir, dirs, files in os.walk(rootdir):
    current_place = os.path.basename(subdir)
    if current_place == "source_data":
        continue

    current_mean_temp = 0.0
    current_mean_wind_speed = 0.0
    current_min_temp = float(sys.maxsize)
    current_max_temp = -sys.maxsize - 1.0
    current_min_wind_speed = float(sys.maxsize)
    current_max_wind_speed = -sys.maxsize - 1.0
    total_entries = 0
    for file in files:
        with open(os.path.join(subdir, file)) as f:
            data = json.load(f)
            hourly = data["hourly"]
            total_entries += len(hourly)
            for hour in hourly:
                temp = float(hour["temp"])
                wind_speed = float(hour["wind_speed"])
                mean_temp += temp
                mean_wind_speed += wind_speed
                current_mean_temp += temp
                current_mean_wind_speed += wind_speed
                if max_temp < temp:
                    max_temp = float(temp)
                    warmest_place = current_place
                if min_temp > temp:
                    min_temp = float(temp)
                    coldest_place = current_place
                if max_wind_speed < wind_speed:
                    max_wind_speed = float(wind_speed)
                    windiest_place = current_place
                if min_wind_speed > wind_speed:
                    min_wind_speed = float(wind_speed)
                if current_max_temp < temp:
                    current_max_temp = float(temp)
                if current_min_temp > temp:
                    current_min_temp = float(temp)
                if current_max_wind_speed < wind_speed:
                    current_max_wind_speed = float(wind_speed)
                if current_min_wind_speed > wind_speed:
                    current_min_wind_speed = float(wind_speed)

    current_mean_temp = current_mean_temp / len(hourly)
    current_mean_wind_speed = current_mean_wind_speed / len(hourly)
    city_element = ET.Element(sanitize_tag_name(current_place))
    city_element.set('mean_temp', str(round(current_mean_temp, 2)))
    city_element.set('mean_wind_speed', str(round(current_mean_wind_speed, 2)))
    city_element.set('min_temp', str(round(current_min_temp, 2)))
    city_element.set('min_wind_speed', str(round(current_min_wind_speed, 2)))
    city_element.set('max_temp', str(round(current_max_temp, 2)))
    city_element.set('max_wind_speed', str(round(current_max_wind_speed, 2)))

    cities.append(city_element)
    city_count += 1

mean_temp = mean_temp / (city_count * 24.0)
mean_wind_speed = mean_wind_speed / (city_count * 24.0)


summary.set('mean_temp', str(round(mean_temp, 2)))
summary.set('mean_wind_speed', str(round(mean_wind_speed, 2)))
summary.set('coldest_place', coldest_place)
summary.set('warmest_place', warmest_place)
summary.set('windiest_place', windiest_place)

xml_str = ET.tostring(weather, encoding='utf-8', method='xml')

parsed_xml = minidom.parseString(xml_str)
pretty_xml_str = parsed_xml.toprettyxml(indent="  ")

with open("result.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml_str)
