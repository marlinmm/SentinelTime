import rasterio.mask
import rasterio.plot
from SentinelTime.data_preprocessing import *
from SentinelTime.xml_extract import *


def mask_tif(shape_path, main_dir, results_dir):
    """
    Function to clip raster files with given polygon (ROI) to reduce file size
    :param shape_path: string
        Path to shapfile for ROI
    :param main_dir: string
        Path to main directory containing the original raster files or subdirectories containing the original raster
        files
    :param results_dir: string
        Path to Output directory where results should be stored
    :return: list
        Returns list of directories, where the subsets for each polarization and flight direction are stored
    """
    file_name_list, path_list = eliminate_nanoverlap(main_dir, shape_path)

    rel_orbit_number_list = []
    for i, name in enumerate(file_name_list):
        filename = name[0:28] + "manifest.safe"
        path_name = path_list[i]
        rel_orbit_number = "_" + xml_extract(path=path_name, file=filename)
        rel_orbit_number_list.append(rel_orbit_number)

    shapes = import_polygons(shape_path)

    # Print info, what step is currently processed:
    print("Cliping overlapping files to ROI...")

    # Create necessary folder for the output:
    VH_folder = results_dir + "VH/"
    VH_Asc_folder = VH_folder + "Asc/"
    VH_Desc_folder = VH_folder + "Desc/"
    if not os.path.exists(VH_folder):
        os.mkdir(VH_folder)
        os.mkdir(VH_Asc_folder)
        os.mkdir(VH_Desc_folder)

    VV_folder = results_dir + "VV/"
    VV_Asc_folder = VV_folder + "Asc/"
    VV_Desc_folder = VV_folder + "Desc/"
    if not os.path.exists(VV_folder):
        os.mkdir(VV_folder)
        os.mkdir(VV_Asc_folder)
        os.mkdir(VV_Desc_folder)

    # Iterate through all files, which overlap with the ROI (return from "eliminate_nanoverlap" function)
    for i, file in enumerate(file_name_list):
        file_name = path_list[i] + file_name_list[i]

        if os.path.exists(VH_Asc_folder + file[10:len(file)]):
            continue
        if os.path.exists(VH_Desc_folder + file[10:len(file)]):
            continue
        if os.path.exists(VV_Asc_folder + file[10:len(file)]):
            continue
        if os.path.exists(VV_Desc_folder + file[10:len(file)]):
            continue

        # Clip files to extent of ROI:
        src1 = rio.open(file_name)
        out_image, out_transform = rio.mask.mask(src1, [shapes[0]], all_touched=0, crop=True, nodata=np.nan)
        out_meta = src1.meta
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

        # Write subsets to corresponding folders and rename files to be sorted by date:
        flight_dir = file_name_list[i][file_name_list[i].index("___") + 3:file_name_list[i].index("___") + 4]
        polarization = file_name_list[i][file_name_list[i].index("grd") - 3:file_name_list[i].index("grd") - 1]
        if polarization == "VH":
            if flight_dir == "A":
                with rasterio.open(
                        VH_Asc_folder + file[10:len(file)-4] + "_" + file[0:3] + rel_orbit_number_list[i] + ".tif", "w",
                        **out_meta) as dest:
                    dest.write(out_image)
            if flight_dir == "D":
                with rasterio.open(
                        VH_Desc_folder + file[10:len(file)-4] + "_" + file[0:3] + rel_orbit_number_list[i] + ".tif",
                        "w", **out_meta) as dest:
                    dest.write(out_image)
        if polarization == "VV":
            if flight_dir == "A":
                with rasterio.open(
                        VV_Asc_folder + file[10:len(file)-4] + "_" + file[0:3] + rel_orbit_number_list[i] + ".tif", "w",
                        **out_meta) as dest:
                    dest.write(out_image)
            if flight_dir == "D":
                with rasterio.open(
                        VV_Desc_folder + file[10:len(file)-4] + "_" + file[0:3] + rel_orbit_number_list[i] + ".tif",
                        "w", **out_meta) as dest:
                    dest.write(out_image)
    return [VH_Asc_folder, VH_Desc_folder, VV_Asc_folder, VV_Desc_folder]


def raster_stack(shape_path, main_dir, results_dir, overwrite):
    """
    This function stacks the clipped raster files to one raster time series stack for each polarization and flight
    direction
    :param overwrite:
    :param shape_path: string
        Path to shapfile for ROI
    :param main_dir: string
        Path to main directory containing the original raster files or subdirectories containing the original raster
        files
    :param results_dir:
        Path to Output directory where results should be stored
    """

    result_folder = mask_tif(shape_path, main_dir, results_dir)
    print("Creating time series stack...")

    for folder in result_folder:
        file_list = extract_files_to_list(path_to_folder=folder, datatype=".tif", path_bool=True)
        # Read metadata of first file
        with rasterio.open(file_list[0]) as src0:
            meta = src0.meta

        # Update meta to reflect the number of layers
        meta.update(count=len(file_list))

        # Read each layer and write it to stack
        if "VH" in folder and "Asc" in folder:
            stack_name = "VH_Asc_stack.tif"
        if "VH" in folder and "Desc" in folder:
            stack_name = "VH_Desc_stack.tif"
        if "VV" in folder and "Asc" in folder:
            stack_name = "VV_Asc_stack.tif"
        if "VV" in folder and "Desc" in folder:
            stack_name = "VV_Desc_stack.tif"

        # Check if file already exists, and depending on overwrite decision, overwrite or tell user, that file exists
        if not overwrite:
            if os.path.exists(results_dir + stack_name):
                print("File already exists")
                continue

        # Write rasterstacks for all polarizations and flight directions:
        with rasterio.open(results_dir + stack_name, 'w', **meta) as dst:
            for i, layer in enumerate(file_list, start=1):
                with rasterio.open(layer) as src1:
                    dst.write_band(i, src1.read(1))
