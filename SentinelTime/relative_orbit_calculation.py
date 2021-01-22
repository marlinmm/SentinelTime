def calculate_relative_orbit_S1(absolute_orbit_number, S1_satellite):
    """

    :param absolute_orbit_number: absolute orbit number stated in GRD filename right after the last datetime statement
    :param S1_satellite: parameter for S1 satellite (S1A or S1B)
    :return: relative orbit nuber
    """
    # Calculate Relative Orbit Number from Absolute Orbit Number:
    # Sentinel-1A
    if S1_satellite == "A":
        relative_orbit_number = ((absolute_orbit_number - 73) % 175) + 1
    # Sentinel-1B
    if S1_satellite == "B":
        relative_orbit_number = ((absolute_orbit_number - 27) % 175) + 1
    # Source: https://forum.step.esa.int/t/sentinel-1-relative-orbit-from-filename/7042 (Peter Meadows, Member of the
    # Mission Performance Centre)
    return relative_orbit_number
