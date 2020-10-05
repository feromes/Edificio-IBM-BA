import pdal, json
import geopandas as gpd

gdf_ibm = gpd.read_file('gis/lote-edificio-IBM.shp')

for i, r in gdf_ibm.iterrows():

    s = r.geometry
    bounds = ([s.bounds[0], s.bounds[2]], [s.bounds[1], s.bounds[3]])

    ept = [
        {
          "type": "readers.ept",
          "filename": "https://ept-m3dc-pmsp.s3-sa-east-1.amazonaws.com/ept.json",
          "bounds": str(bounds)
        },
        {
            "type":"filters.crop",
            "polygon":s.wkt
        },
        {
            "type":"writers.las",
            "compression":"lazip",
            "filename": 'LiDAR/Lote-IBM.laz'
        }
    ]

    pipeline = pdal.Pipeline(json.dumps(ept))
    pipeline.validate()
    n_points = pipeline.execute()
    print(f'Pipeline selected {n_points} points')