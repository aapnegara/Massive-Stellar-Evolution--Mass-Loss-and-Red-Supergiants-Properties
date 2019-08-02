!#/bin/bash

cd create_zams_ekstrom_12M0
./clean
./mk
./rn
cd ../

cd create_zams_ekstrom_15M0
./clean
./mk
./rn
cd ../

cd create_zams_ekstrom_20M0
./clean
./mk
./rn
cd ../

cd create_zams_ekstrom_25M0
./clean
./mk
./rn
cd ../

cd create_zams_ekstrom_30M0
./clean
./mk
./rn
cd ../

cd create_zams_ekstrom_35M0
./clean
./mk
./rn
cd ../

echo "Terminou!"
