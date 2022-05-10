from os import path
import xml.etree.ElementTree as ET
from haversine import haversine

#constants
KML_FILENAME = "task_2_sensor.kml"
KML_FILE = path.join(KML_FILENAME)
UPDATED_KML_FILENAME="task_2_sensor_filtered.kml"
UPDATED_KML_FILE = path.join(UPDATED_KML_FILENAME)
ARBITRARY_COORDINATE_DIFFERENCE_CHECK = 0.005

def process_kml():
    new_coordinates_for_distance = filter_kml()
    return calculate_distance(new_coordinates_for_distance)


def filter_kml():
    tree  = ET.parse(KML_FILE)
    root = tree.getroot()

    coordinates = tree.find(".//{http://www.opengis.net/kml/2.2}coordinates").text.strip().split(" ")
    new_coordinates = []
    new_coordinates.append((float(coordinates[0].split(",")[0]), float(coordinates[0].split(",")[1]), float(coordinates[0].split(",")[2])))
    for coordinate in coordinates:
        coordinate_x_y_z_values = coordinate.split(",")
        coordinate_tuple = (float(coordinate_x_y_z_values[0]), float(coordinate_x_y_z_values[1]), float(coordinate_x_y_z_values[2]))
        if is_coordinate_distance_not_too_big(new_coordinates[-1],coordinate_tuple):
            new_coordinates.append(coordinate_tuple)

    write_updated_kml_file(tree,root,new_coordinates)
    
    return new_coordinates


def write_updated_kml_file(tree,root,new_coordinates):
    tree.find(".//{http://www.opengis.net/kml/2.2}coordinates").text=" ".join([",".join([str(coord) for coord in coords]) for coords in new_coordinates])
    ET.register_namespace('', 'http://www.opengis.net/kml/2.2')
    tree = ET.ElementTree(root)
    tree.write(UPDATED_KML_FILE, xml_declaration=True, encoding="UTF-8", method="xml")


def is_coordinate_distance_not_too_big(previous_position, current_position):
    return (abs(previous_position[0] - current_position[0]) < ARBITRARY_COORDINATE_DIFFERENCE_CHECK 
        and abs(previous_position[1] - current_position[1]) < ARBITRARY_COORDINATE_DIFFERENCE_CHECK)


def distance_travelled(starting_coord, landing_coord):
    starting_coord_latitude_longtitude = starting_coord[0:-1][::-1]
    current_coord_latitude_longtitude = landing_coord[0:-1][::-1]
    return haversine(starting_coord_latitude_longtitude, current_coord_latitude_longtitude, unit='km')


def calculate_distance(coordinates):
    total_distance_travelled_km = 0.0
    for index in range(len(coordinates)-1):
        total_distance_travelled_km += distance_travelled(coordinates[index], coordinates[index+1])
    return total_distance_travelled_km


if __name__ == "__main__":
    print("Distance travelled: " + str(process_kml()))
