import webbrowser
import folium
import pandas
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt

def read_file():
    lst = []
    file = open('locations1.txt', 'r', encoding='utf-16')
    for line in file:
        lst.append(line)
    return lst

def create_map_html():
    year = input("Please enter a year you would like to have a map for:")
    location = input("Please enter your location (format: lat, long):")
    print("Map is generating...")
    print("Please wait...")

    loc = []
    loc.append(location.split(', '))


    map = folium.Map(location=[float(loc[0][0]), float(loc[0][1])])

    lst = []
    lst1 = []
    lst2 = []
    lst3 = []
    lst4 = []
    for i in read_file():
        if year in i:
            lst.append(i.split('\t'))
    for i in lst:
        if "(" not in i[-1] and "�" not in i[-1]:
            lst1.append([i[0], i[-1][:-1]])
    for i in lst1:
        if len(i[-1].split(' ')) > 3:
            if [i[0].split('(')[0], i[-1].split(' ')[-2:]] not in lst2:
                lst2.append([i[0].split('(')[0], i[-1].split(' ')[-2:]])
    for i in lst2:
        lst3.append([i[0], i[1][0] + " " + i[1][1]])

    for i in lst3:
        geolocator = Nominatim(user_agent="test")
        location = geolocator.geocode(i[-1])
        lst4.append([i[0], [location.latitude, location.longitude]])

    lst5 = []
    lst6 = []
    lst7 = []
    lst8 = []
    list_of_markers = []
    R = 6372.8
    lat1 = float(loc[0][0])
    lon1 = float(loc[0][1])

    for i in lst4:
        dLat = radians(i[1][0] - lat1)
        dLon = radians(i[1][1] - lon1)
        lat1 = radians(lat1)
        lat2 = radians(i[1][0])

        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))
        lst5.append(R*c)

    H = []
    j = 0
    for i in lst4:
        lst6.append(i[1])
    while j != lst5.index(lst5[-1]):
        H.append([lst5[j],lst6[j]])
        j += 1


    for i in lst5:
        while len(lst7) != 5:
            lst7.append(min(lst5))
            lst5.remove(min(lst5))
    
    for i in lst7:
        for k in H:
            if i in k:
                lst8.append(k[1])
    for i in lst8:
        for k in lst4:
            if i in k:
                list_of_markers.append(k)
                
    for i in list_of_markers:
        map.add_child(folium.Marker(location=i[-1],
                        popup=i[0],
                        icon=folium.Icon()))
    map.save('Map_5.html')
    return webbrowser.open('Map_5.html', new=2)
print(create_map_html())
