import xml.etree.ElementTree as ET
from SentinelTime.data_preprocessing import *


def xml_extract(path, file):

    root = ET.parse(path + file).getroot()

    for rel_orbit in root.iter('{http://www.esa.int/safe/sentinel-1.0}relativeOrbitNumber'):
        rel_orbit_number = rel_orbit.text
    return rel_orbit_number
