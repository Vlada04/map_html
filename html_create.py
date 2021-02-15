import webbrowser
import folium
import pandas
from geopy.geocoders import Nominatim

def read_file():
    '''
    
    '''
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

    for i in lst4:
        map.add_child(folium.Marker(location=i[-1],
                        popup=i[0],
                        icon=folium.Icon()))
    map.save('Map_5.html')
    return webbrowser.open('Map_5.html', new=2)

print(create_map_html())
