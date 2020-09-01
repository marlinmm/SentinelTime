import fiona
import rasterio.mask
import numpy as np
from osgeo import gdal
import rasterio.plot

with fiona.open("/home/ni82xoj/Ortho_SALDI/Test_shapefiles_KNP/Trig_export_KNP_reprojected_1000m_buffer_102568.shp",
                "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]
    shapes = np.array_split(shapes, 89)
    #for a, stations in enumerate(shapes):
    #print(a, stations)
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