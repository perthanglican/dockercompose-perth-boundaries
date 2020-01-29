#!/bin/bash -x

loadshape()
{
  f="$PWD/$1"
  name="$2"
  srid="$3"
  tempd=$(mktemp -d)
  (cd "$tempd" && unzip "$f" && shp2pgsql -s "$srid" *.shp "$name" | psql -U postgres perth && rm -rf "$tempd")
}

apt-get update && apt-get -y install unzip

dropdb -U postgres perth
createdb -U postgres perth
echo 'CREATE EXTENSION postgis;' | psql -U postgres perth

loadshape Intersections.zip intersections 4326
loadshape Road_Network.zip road_network 4326
loadshape LocalitiesLGATE_234.zip localities 3857
loadshape LocalGovernmentAuthorityLGABoundariesLGATE_233.zip lgas 3857

