import cv2
import pathlib
import shutil

import PySimpleGUI as sg
import os

import numpy as np
import pandas
import folium
import math

from API.ItineraryAPI.Location import Location
from Service.ObjectiveVisit import ObjectiveVisit
from Service.ServiceMain import ServiceMain
import operator
from PIL import Image

service=ServiceMain()


def searchByTextAlgorithm(text):
    # do stuff
    print("RUNNING TEXT ALGORITHM FOR :")
    print(text)
    # get result
    locations=service.getTextLocation(text)
    # locations = ["Malibu", "California", "Sri Lanka"]
    searchByTextResultWindow(locations)


def searchByImageAlgorithm(imageLocation):
    # do stuff
    print("RUNNING IMAGE ALGORITHM FOR :")
    print(imageLocation)
    # get result
    locations=service.getImageLocation(imageLocation)
    # locations = ["Malibu", "California", "Sri Lanka"]
    searchByTextResultWindow(locations)


def getTextObj(c, r,list):
    try:
        el=list[r]
        if c==0:
            return str(el.location.name)
        if c==1:
            return str(el.no_of_reviews).replace(',',"")
        if c==2:
            return str(el.staying_time)
        if c==3:
            return str(el.description)
        if c==4:
            return str(el.tripadvisor_link)
    except:
        return ""


def getSize(col):
    if col==0:
        return 35
    elif col==1:
        return 15
    elif col==2:
        return 5
    elif col==3:
        return 80
    elif col==4:
        return 20
    elif col==5:
        return 20
    elif col==6:
        return 10

def getObjectivesByImportance(location, param):
    MAX_ROWS, MAX_COLS, COL_HEADINGS = len(param), 5, ('Nume', 'Review', 'Duration', 'Description', 'Link')
    print('max_rows'+str(MAX_ROWS))
    print('max_cols'+str(MAX_COLS))
    # A HIGHLY unusual layout definition
    # Normally a layout is specified 1 ROW at a time. Here multiple rows are being contatenated together to produce the layout
    # Note the " + \ " at the ends of the lines rather than the usual " , "
    # This is done because each line is a list of lists
    layout = [[sg.Text('Select all the great place you want to visit', font='Default 16')]] + \
             [[sg.Text(' ' * 15)] + [sg.Text(s, key=s, enable_events=True, font='Courier 14', size=(8, 1)) for i, s in
                                     enumerate(COL_HEADINGS)]] + \
             [[ sg.Checkbox(r,size=(2,2))] + [sg.Input(getTextObj(c,r,param), justification='r', key=(r, c),size=(getSize(c),1)) for c in
                                        range(MAX_COLS)] for r in range(MAX_ROWS)] + \
             [[sg.Button('Show Route'), sg.Button('Exit')]]

    # Create the window
    window = sg.Window('A Table Simulation', layout, default_element_size=(10, 2), element_padding=(2, 1),
                       return_keyboard_events=True)

    current_cell = (0, 0)
    while True:  # Event Loop
        event, values = window.read()

        if event in (None, 'Exit'):  # If user closed the window
            break
        # if clicked button to dump the table's values
        if event in ('Show Route'):
            print(values)
            window.close()

            for i in range(MAX_ROWS):
                for v in param:
                    if v.location.name==values[i,0] and values[i]==True:
                        print("GOT ONE GOOD")
                        print(values[i,0])
                        print(values[i])
                        v.priority="2"
                if values[i]==False:
                    for v in param:
                        if v.location.name == values[i, 0]:
                            print("GOT ONE GOOD")
                            v.priority = "1"
                            param.remove(v)
            sg.popup_quick_message('Hang on for a moment, this will take a bit to calculate....',
                                   auto_close=True, non_blocking=True)

            print(len(param))
            return param

        elem = window.find_element_with_focus()
        current_cell = elem.Key if elem and type(elem.Key) is tuple else (0, 0)
        r, c = current_cell

        if event.startswith('Down'):
            r = r + 1 * (r < MAX_ROWS - 1)
        elif event.startswith('Left'):
            c = c - 1 * (c > 0)
        elif event.startswith('Right'):
            c = c + 1 * (c < MAX_COLS - 1)
        elif event.startswith('Up'):
            r = r - 1 * (r > 0)
        elif event in COL_HEADINGS:  # Perform a sort if a column heading was clicked
            col_clicked = COL_HEADINGS.index(event)
            try:
                table = [[str(values[(row, col)]) for col in range(MAX_COLS)] for row in range(MAX_ROWS)]

                new_table = sorted(table, key=operator.itemgetter(col_clicked))
            except:
                sg.popup_error('Error in table', 'Your table must contain only ints if you wish to sort by column')
            else:
                for i in range(MAX_ROWS):
                    for j in range(MAX_COLS):
                        window[(i, j)].update(new_table[i][j])
                [window[c].update(font='Any 14') for c in COL_HEADINGS]  # make all column headings be normal fonts
                window[event].update(font='Any 14 bold')  # bold the font that was clicked
        # if the current cell changed, set focus on new cell
        if current_cell != (r, c):
            current_cell = r, c
            window[current_cell].set_focus()  # set the focus on the element moved to
            window[current_cell].update(
                select=True)  # when setting focus, also highlight the data in the element so typing overwrites



def searchRouteByLocationAlgorithm(location, filters):
    print("WE ARE SEARCHING VISITING ROUTES IN ", location)
    print("With these filters ", filters)

    # does magic
    param=service.getObjectivesByLocationAndFilter(location,filters)
    # param = ["Eiffel Tower", "Louvre Museum", "Sena River", "champs-élysées"]

    lista = [el.toString() for el in param]
    print(lista)

    importanceList=getObjectivesByImportance(location,param)

    itinerary,tranz,image=service.getRouteByLocationsAndImportance(importanceList)
    # image=service.getRouteVisualization()
    searchByLocationRouteResult(itinerary,tranz,image)


def showMeTheMap(param):
    lat=[]
    long=[]
    points=[]
    for p in param:
        coord=Location.get_locations_by_query(p)
        print(coord[0].latitude,coord[0].longitude)
        # lat.append(coord[0].latitude)
        # long.append(coord[0].longitude)

        points.append(tuple([coord[0].latitude, coord[0].longitude]))

    # centroid_lat = 16.7
    # centroid_lon = 81.095
    #
    # x = .1
    #
    # n = 10
    #
    # o_lats = np.asarray(lat[0:-2])
    # o_lons = np.asarray(long[0:-2])
    # d_lats = np.asarray(lat[1:-1])
    # d_lons = np.asarray(long[1:-1])
    #
    # df = pandas.DataFrame({'origin_lng': o_lons, 'origin_lat': o_lats,
    #                    'destination_lng': d_lons, 'destination_lat': d_lats})


    print(points)
    ave_lat = sum(p[0] for p in points) / len(points)
    ave_lon = sum(p[1] for p in points) / len(points)

    # Load map centred on average coordinates
    my_map = folium.Map(location=[ave_lat, ave_lon], zoom_start=14)

    # add a markers
    for each in points:
        folium.Marker(each).add_to(my_map)

    # fadd lines
    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(my_map)

    # Save map
    my_map.save("./gpx_berlin_withmarker.html")

    pass


def searchByLocationRouteResult(itinerary,tranz,image):
    # lista=[el.toString() for el in param]
    print(itinerary)
    print(tranz)
    print(image)


    ROOT_DIR = str(pathlib.Path(__file__).parent.parent.parent.parent.absolute()) + "\\GUI\\data\\route.jpeg"

    with open(ROOT_DIR, 'wb') as out_file:
        shutil.copyfileobj(image, out_file)
    lista=[it for it in itinerary]
    listaT=[tr for tr in tranz]


    # image_elem = sg.Image(ROOT_DIR, size=(80, 80))
    # image_elem=sg.Image(filename='', key='image')(data=cv2.imencode('.png', ROOT_DIR)[1].tobytes())


    layout = [
        [sg.Text('We found an amazing route for you..')],
        [sg.Listbox(values=lista, size=(130, 20))],
        [sg.Listbox(values=listaT, size=(130, 20))],
        # [image_elem],
        [sg.Button("Show me on map"), sg.Button('Cancel')]
    ]

    windowTextResults = sg.Window('HOLIday').Layout(layout)
    while True:
        event, values = windowTextResults.Read()
        if event in (None, 'Cancel'):
            windowTextResults.close()
            main()
            print("Goodbye")
            break
        elif event in ("Show me on map"):
            windowTextResults.close()
            # showMeTheMap(param)


# Very basic window.  Return values as a list
def searchByTextResultWindow(locations):
    locations=[loc[::-1] for loc in locations]
    print(locations)
    print(len(locations))
    print(len(locations[0]))

    MAX_ROWS, MAX_COLS, COL_HEADINGS = len(locations), len(locations[0]), ('Name', 'Probability', 'Descr')

    # A HIGHLY unusual layout definition
    # Normally a layout is specified 1 ROW at a time. Here multiple rows are being contatenated together to produce the layout
    # Note the " + \ " at the ends of the lines rather than the usual " , "
    # This is done because each line is a list of lists
    layout = [[sg.Text('Those are you top choices', font='Default 16')]] + \
             [[sg.Text(' ' * 15)] + [sg.Text(s, key=s, enable_events=True, font='Courier 14', size=(8, 1)) for i, s in
                                     enumerate(COL_HEADINGS)]] + \
             [[sg.Checkbox(r, size=(2, 2))] + [
                 sg.Input(locations[r][c], justification='r', key=(r, c), size=(getSize(c), 1)) for c in
                 range(MAX_COLS)] for r in range(MAX_ROWS)] + \
             [[sg.Button('Show Route'), sg.Button('Exit')]]

    # Create the window
    window = sg.Window('A Table Simulation', layout, default_element_size=(10, 2), element_padding=(2, 1),
                       return_keyboard_events=True)

    current_cell = (0, 0)
    while True:  # Event Loop
        event, values = window.read()

        if event in (None, 'Exit'):  # If user closed the window
            break
        # if clicked button to dump the table's values
        if event in ('Show Route'):
            print(values)

            for i in range(MAX_ROWS):
                for v in locations:
                    print(values[i, 0])
                    print(values[i])
                    if v.location.name == values[i, 0] and values[i] == True:
                        window.close()
                        sg.popup_quick_message('Hang on for a moment, this will take a bit to calculate....',
                                               auto_close=True, non_blocking=True)

                        return v.location
                    else:
                        v.priority = "0"



        elem = window.find_element_with_focus()
        current_cell = elem.Key if elem and type(elem.Key) is tuple else (0, 0)
        r, c = current_cell

        if event.startswith('Down'):
            r = r + 1 * (r < MAX_ROWS - 1)
        elif event.startswith('Left'):
            c = c - 1 * (c > 0)
        elif event.startswith('Right'):
            c = c + 1 * (c < MAX_COLS - 1)
        elif event.startswith('Up'):
            r = r - 1 * (r > 0)
        elif event in COL_HEADINGS:  # Perform a sort if a column heading was clicked
            col_clicked = COL_HEADINGS.index(event)
            try:
                table = [[str(values[(row, col)]) for col in range(MAX_COLS)] for row in range(MAX_ROWS)]

                new_table = sorted(table, key=operator.itemgetter(col_clicked))
            except:
                sg.popup_error('Error in table', 'Your table must contain only ints if you wish to sort by column')
            else:
                for i in range(MAX_ROWS):
                    for j in range(MAX_COLS):
                        window[(i, j)].update(new_table[i][j])
                [window[c].update(font='Any 14') for c in COL_HEADINGS]  # make all column headings be normal fonts
                window[event].update(font='Any 14 bold')  # bold the font that was clicked
        # if the current cell changed, set focus on new cell
        if current_cell != (r, c):
            current_cell = r, c
            window[current_cell].set_focus()  # set the focus on the element moved to
            window[current_cell].update(
                select=True)  # when setting focus, also highlight the data in the element so typing overwrites


def searchRouteByLocationWindow(location,filter):
    layoutOperation = [
        [sg.Text('What place do you want to explore ?')],
        [sg.InputText(location)], [],
        # [sg.Text('By what do you want to travel ?')],
        # [sg.Checkbox('Personal car'), sg.Checkbox('On foot', default=True), sg.Checkbox("Public transportation")],
        [sg.Text('What are your interests ?')],
        [sg.Listbox(values=filter, size=(30, 10), select_mode="multiple")],
        [sg.Button('Search for me'), sg.Button('Cancel')]
    ]
    windowOperation = sg.Window('Text it out').Layout(layoutOperation)

    while True:
        eventOperation, valuesOperation = windowOperation.Read()
        if eventOperation in (None, 'Cancel'):
            windowOperation.close()
            main()
            break
        elif eventOperation in ('Search for me'):
            windowOperation.close()

            print(valuesOperation)
            sg.popup_quick_message('Hang on for a moment, this will take a bit to calculate....',
                                   auto_close=True, non_blocking=True)
            searchRouteByLocationAlgorithm(valuesOperation[0], valuesOperation[1])


def searchByImageTextAlgorithm(text, path):
    print("RUNNING TEXT & IMAGE ALGORITHM FOR :")
    print(text)
    print(path)

    locations=service.getImageTextLocation(text,path)
    # get result
    # locations = ["Malibu", "California", "Sri Lanka"]

    searchByTextResultWindow(locations)


def openWindowImageTextSearch():
    print('Text & Image search')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))[0:-7] + "\\data\\blohsaved.png"
    print(ROOT_DIR)
    image_elem = sg.Image(ROOT_DIR,size=(80,80))

    layoutOperation = [
        [sg.Text('A few words to guide us..')],
        [sg.InputText('Couple of words')],[],
        [sg.Text('An image says what a thousand words can\'t..')],
        [sg.Text('The image :'), sg.InputText('path'), sg.FileBrowse()],
        [image_elem],
        [sg.Button('Search for me'), sg.Button('Cancel')]
    ]
    windowOperation = sg.Window('Tell us',resizable=True).Layout(layoutOperation)

    while True:
        eventOperation, valuesOperation = windowOperation.Read(timeout=50)
        # print(valuesOperation)
        if eventOperation in (None, 'Cancel'):
            windowOperation.close()
            main()
            break
        elif eventOperation in ('Search for me'):
            windowOperation.close()
            print(valuesOperation[1])
            sg.popup_quick_message('Hang on for a moment, this will take a bit to calculate....',
                                   auto_close=True, non_blocking=True)

            searchByImageTextAlgorithm(valuesOperation[0], valuesOperation[1])

        if valuesOperation[1] != "path":
            image_elem.update(valuesOperation[1])



def openWindowTextSearch():
    print('Text search')
    layoutOperation = [
        [sg.Text('A few words to guide us..')],
        [sg.InputText('Couple of words')],
        [sg.Button('Search for me'), sg.Button('Cancel')]
    ]
    windowOperation = sg.Window('Text it out').Layout(layoutOperation)

    while True:
        eventOperation, valuesOperation = windowOperation.Read()
        if eventOperation in (None, 'Cancel'):
            windowOperation.close()
            main()
            break
        else:
            windowOperation.close()
            sg.popup_quick_message('Hang on for a moment, this will take a bit to calculate....',
                                   auto_close=True, non_blocking=True)

            searchByTextAlgorithm(valuesOperation[0])


def openWindowImageSearch():
    print('Image search')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))[0:-7] + "\\data\\blohsaved.png"
    print(ROOT_DIR)
    image_elem = sg.Image(ROOT_DIR)
    layoutOperation = [
        [sg.Text('An image says what a thousand words can\'t..')],
        [sg.Text('The image :'), sg.InputText('path'), sg.FileBrowse()],
        [sg.Button('Search for me'), sg.Button('Cancel')],
        [image_elem]
    ]
    windowOperation = sg.Window('Text it out').Layout(layoutOperation)

    while True:
        eventOperation, valuesOperation = windowOperation.Read(timeout=50)
        if eventOperation in (None, 'Cancel'):
            windowOperation.close()
            main()
            break
        elif eventOperation in ('Search for me'):
            windowOperation.close()
            print(valuesOperation[0])
            sg.popup_quick_message('Hang on for a moment, this will take a bit to calculate....',
                                   auto_close=True, non_blocking=True)

            searchByImageAlgorithm(valuesOperation[0])

        if valuesOperation[0] != "path":
            try:
                image_elem.update(valuesOperation[0])
            except:

                im = Image.open(valuesOperation[0])
                im.save(valuesOperation[0].split('.jpg')[0]+'.png')
                image_elem.update(valuesOperation[0].split('.jpg')[0]+'.png')



def openWindowRoutesSearch():
    print('Route search')
    layoutOperation = [
        [sg.Text('What place do you want to explore ?')],
        [sg.InputText('location')],
        [sg.Button('HERE !'), sg.Button('Cancel')]
    ]
    windowOperation = sg.Window('Where ?').Layout(layoutOperation)

    while True:
        eventOperation, valuesOperation = windowOperation.Read()
        if eventOperation in (None, 'Cancel'):
            windowOperation.close()
            main()
            break
        else:
            windowOperation.close()
            filter=service.getFilters()
            print(filter)
            sg.popup_quick_message('Hang on for a moment, this will take a bit to calculate....',
                                   auto_close=True, non_blocking=True)

            searchRouteByLocationWindow(valuesOperation[0],filter)


sg.ChangeLookAndFeel('Dark')
sg.SetOptions(element_padding=(5, 5), button_element_size=(20, 2), auto_size_buttons=False,
              button_color=('white', 'firebrick4'))
layout = [
    [sg.Text('Let us plan an awesome holiday for you..')],
    [sg.Button('Search only with text'), sg.Button('Search only with image'), sg.Button('Search with image & text'), sg.Button('Create a route')],
    [sg.Button('Cancel')]
]
window = sg.Window('HOLIday').Layout(layout)



def main():


    try:
        window.enable()
    except(Exception):
        print("NOW")

    while True:
        event, values = window.Read()
        if event in (None, 'Cancel'):
            print("Goodbye")
            break

        if event in ('Search with image & text'):
            window.disable()
            openWindowImageTextSearch()

        if event in ('Search only with text'):
            window.disable()
            openWindowTextSearch()

        if event in ('Search only with image'):
            window.disable()
            openWindowImageSearch()

        if event in ('Create a route'):
            window.disable()
            openWindowRoutesSearch()


main()


