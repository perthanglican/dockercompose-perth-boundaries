#!/bin/bash -x

loadshape()
{
  f="$PWD/$1"
  name="$2"
  srid="$3"
  tempd=$(mktemp -d)
  (cd "$tempd" && unzip "$f" && shp2pgsql -s "$srid" *.shp "$name" | psql -U postgres -h db perth && rm -rf "$tempd")
}

export PGPASSWORD=postgres
dropdb -h db -U postgres perth
createdb -h db -U postgres perth
echo 'CREATE EXTENSION postgis;' | psql -h db -U postgres perth

gunzip -c Intersections.geojson.gz > Intersections.geojson
ogr2ogr -lco geometry_name=geom -lco fid=gid -t_srs EPSG:3857 -f "PostgreSQL" "PG:dbname=perth host=db user=postgres password=postgres" Intersections.geojson
rm Intersections.geojson

gunzip -c Road_Network.geojson.gz > Road_Network.geojson
ogr2ogr -lco geometry_name=geom -lco fid=gid -t_srs EPSG:3857 -f "PostgreSQL" "PG:dbname=perth host=db user=postgres password=postgres" Road_Network.geojson
rm Road_Network.geojson

loadshape LocalitiesLGATE_234.zip localities 3857
loadshape LocalGovernmentAuthorityLGABoundariesLGATE_233.zip lgas 3857

# snap the localities and LGAs
echo 'update localities set geom=st_snaptogrid(geom, 1);' | PGPASSWORD=postgres psql -U postgres -h db -d perth
echo 'update lgas set geom=st_snaptogrid(geom, 1);' | PGPASSWORD=postgres psql -U postgres -h db -d perth
