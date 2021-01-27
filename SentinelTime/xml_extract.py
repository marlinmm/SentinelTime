import xml.etree.ElementTree as ET
from SentinelTime.data_preprocessing import *


def xml_extract(path, file):
    # file_list, path_list = create_overlap_file_list(path_to_folder=path_to_folder, datatype=".safe")

    # Iterate through raster file list and import each file
    # counter = 0
    # for i, files in enumerate(file_list):

    root = ET.parse(path + file).getroot()

    for rel_orbit in root.iter('{http://www.esa.int/safe/sentinel-1.0}relativeOrbitNumber'):
        rel_orbit_number = rel_orbit.text
    return rel_orbit_number
