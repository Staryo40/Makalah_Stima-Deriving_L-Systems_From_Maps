# Tugas Makalah Stima

conda info --envs  
conda create -n geoenv -c conda-forge osmium-tool
conda activate geoenv
conda install -c conda-forge osmium-tool
conda install -c conda-forge gdal
osmium --version
osmium export your-map.osm.pbf -o output.geojson -f geojson