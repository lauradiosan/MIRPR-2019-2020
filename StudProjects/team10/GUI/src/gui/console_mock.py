from API.ItineraryAPI.Location import Location

add_loc = True
to_visit = []
while add_loc:
    add_loc = True if input("Add location? (Y|N)") == "Y" else False
    if not add_loc: break
    location_query = input("Give a location: ")
    locations = Location.get_locations_by_query(location_query)
    for l in locations:
        print(locations.index(l), " ", l)
    choice = int(input("Select one:"))
    to_visit.append(locations[choice])
