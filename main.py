import webbrowser
import folium
import pandas
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt

def read_file():
    '''
    Read file with films base
    >>> print(type(read_file()))
    <class 'list'>
    '''
    lst = []
    file = open('locations1.txt', 'r', encoding='utf-16')
    for line in file:
        lst.append(line)
    return lst


def create_map_html():
    '''
    Create html map with films of given year
    >>> print(create_map_html())
    True
    '''
    year = input("Please enter a year you would like to have a map for:")
    location = input("Please enter your location (format: lat, long):")
    print("Map is generating...")
    print("Please wait...")

    loc = []
    loc.append(location.split(', '))

    map = folium.Map(location=[float(loc[0][0]), float(loc[0][1])])

    lst = []
    lst_of_movies = []
    lst2 = []
    sorted_lst_of_movies = []
    list_with_coordin = []
    for i in read_file():
        if year in i:
            lst.append(i.split('\t'))
    for i in lst:
        if "(" not in i[-1] and "�" not in i[-1]:
            lst_of_movies.append([i[0], i[-1][:-1]])
    for i in lst_of_movies:
        if len(i[-1].split(' ')) > 3:
            if [i[0].split('(')[0], i[-1].split(' ')[-2:]] not in lst2:
                lst2.append([i[0].split('(')[0], i[-1].split(' ')[-2:]])
    for i in lst2:
        sorted_lst_of_movies.append([i[0], i[1][0] + " " + i[1][1]])

    for i in sorted_lst_of_movies:
        geolocator = Nominatim(user_agent="test")
        location = geolocator.geocode(i[-1])
        list_with_coordin.append([i[0], [location.latitude, location.longitude]])

    lst_of_len = []
    lst6 = []
    limited_list = []
    lst8 = []
    list_of_markers = []
    R = 6372.8
    lat1 = float(loc[0][0])
    lon1 = float(loc[0][1])

    for i in list_with_coordin:
        dLat = radians(i[1][0] - lat1)
        dLon = radians(i[1][1] - lon1)
        lat1 = radians(lat1)
        lat2 = radians(i[1][0])

        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))
        lst_of_len.append(R*c)

    zipped_lst = []
    j = 0
    for i in list_with_coordin:
        lst6.append(i[1])
    while j != lst_of_len.index(lst_of_len[-1]):
        zipped_lst.append([lst_of_len[j],lst6[j]])
        j += 1


    for i in lst_of_len:
        while len(limited_list) != 5:
            limited_list.append(min(lst_of_len))
            lst_of_len.remove(min(lst_of_len))
    
    for i in limited_list:
        for k in zipped_lst:
            if i in k:
                lst8.append(k[1])
    for i in lst8:
        for k in list_with_coordin:
            if i in k:
                list_of_markers.append(k)

    for i in list_of_markers:
        map.add_child(folium.Marker(location=i[-1],
                        popup=i[0],
                        icon=folium.Icon(color='green')))

    fg_pp = folium.FeatureGroup(name="Population")

    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                    encoding='utf-8-sig').read(),
                    style_function=lambda x: {'fillColor':'green'
    if x['properties']['POP2005'] < 10000000
    else 'blue' if 10000000 <= x['properties']['POP2005'] < 20000000
    else 'red'}))
    map.add_child(fg_pp)
    
    map.save('Map_of_films.html')
    return webbrowser.open('Map_of_films.html', new=2)

print(create_map_html())