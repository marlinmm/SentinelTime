import fiona
import rasterio.mask
import numpy as np
from osgeo import gdal
import rasterio.plot
from SentinelTime.data_preprocessing import *


def eliminate_non_overlap(sen_directory, shape_path):
    eliminate_nanoverlap(sen_directory, shape_path)

def mask_tiff ():
    with fiona.open("G:/Shapes/Polygons/extend_of_points.shp",
                "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
        shapes = np.array_split(shapes, 89)
        with rasterio.open(r'/geonfs03_vol1/01_DMC_South_Africa/06_ORTHO/01_KNP/02_25cm/vrt/KNP_25cm__compressed_mosaic.vrt') as raster_vrt:
            # rasterio.plot.show(raster_vrt)
            out_image, out_transform = rasterio.mask.mask(raster_vrt, shapes[82], crop=True)
            out_meta = raster_vrt.meta

            # Driver: "VRT" or "GTiff"?
            out_meta.update({"driver": "GTiff",
                             "height": out_image.shape[1],
                             "width": out_image.shape[2],
                             "transform": out_transform})

        with rasterio.open(
                "/home/ni82xoj/Ortho_SALDI/Outtest/Station_masked"
                + str(82) + ".tif", "w", **out_meta) as dest:
            dest.write(out_image)

def main():
    sen_directory = "G:/Processed/processed_existing/VH"
    sen_overlap_dir = "G:/Processed/processed_existing/VH_overlap"
    shape_path = "G:/Shapes/Polygons/extend_of_points.shp"
    #eliminate_non_overlap(sen_directory=sen_directory, shape_path=shape_path)



if __name__ == '__main__':
    main()
