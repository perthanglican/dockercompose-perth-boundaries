#!/bin/bash -x

loadshape()
{
  f="$PWD/$1"
  srid="$2"
  tempd=$(mktemp -d)
  (cd "$tempd" && unzip "$f" && shp2pgsql -s "$srid" *.shp | psql -U postgres perth && rm -rf "$tempd")
}

apt-get update && apt-get -y install unzip

dropdb -U postgres perth
createdb -U postgres perth
echo 'CREATE EXTENSION postgis;' | psql -U postgres perth

loadshape Intersections.zip 3857
loadshape Road_Network.zip 3857
loadshape LocalitiesLGATE_234.zip 4283
loadshape LocalGovernmentAuthorityLGABoundariesLGATE_233.zip 4283

