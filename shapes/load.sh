dropdb -U postgres perth
createdb -U postgres perth
echo 'CREATE EXTENSION postgis;' | psql -U postgres perth
shp2pgsql -s 3857 IntersectionsMRWA_510.shp | psql -U postgres perth
shp2pgsql -s 3857 RoadNetworkMRWA_514.shp | psql -U postgres perth
shp2pgsql -s 4283 LocalitiesLGATE_008.shp | psql -U postgres perth
shp2pgsql -s 4283 LocalGovernmentAuthorityLGABoundariesLGATE_006.shp | psql -U postgres perth

