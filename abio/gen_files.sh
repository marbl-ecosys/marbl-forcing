#!/bin/bash -e

DATE=`date "+%y%m%d"`
ORIG_FILE=/glade/campaign/cesm/cesmdata/inputdata/lnd/clm2/isotopes/atm_delta_C14_CMIP6_3x1_global_1850-2015_yearly_v2.0_c190528.nc
OUTPUT_DIR=/glade/work/mlevy/cesm_inputdata

rm -f ../atm_delta_C14_CMIP6*.nc

for sector in `seq 1 3`
do
  OUT_FILE=${OUTPUT_DIR}/atm_delta_C14_CMIP6_sector${sector}_global_1850-2015_yearly_v2.0_c${DATE}.nc
  # (1) pull out sector number ${sector}
  ncks -F -d sector,${sector} ${ORIG_FILE} ${OUT_FILE}
  # (2) average over single sector (i.e. remove sector dim from data)
  ncwa -O -a sector ${OUT_FILE} ${OUT_FILE}
  # (3) make time an unlimited dimesnion
  ncks -O --mk_rec_dmn time -x -v sector ${OUT_FILE} ${OUT_FILE}
  # (4) pull out first and last time levels to get Jan 1, 1850 and Jan 1, 2016 dates
  ncks -F -d time,1 ${OUT_FILE} .tmp_pre.nc
  ncap2 -O -F -s 'time(1)=0.0' .tmp_pre.nc .tmp_pre.nc
  ncks -F -d time,166 ${OUT_FILE} .tmp_post.nc
  ncap2 -O -F -s 'time(1)=166.0' .tmp_post.nc .tmp_post.nc
  # (5) concatenate all the files
  ncrcat -O .tmp_pre.nc ${OUT_FILE} .tmp_post.nc ${OUT_FILE}
  # (6) update time bounds
  ncap2 -O -F -s 'bounds_time(1,2)=0.5;bounds_time(2,1)=0.5' ${OUT_FILE} ${OUT_FILE}
  ncap2 -O -F -s 'bounds_time(167,2)=165.5;bounds_time(168,1)=165.5' ${OUT_FILE} ${OUT_FILE}
  rm -f .tmp_pre.nc .tmp_post.nc

  echo "Done processing sector ${sector}:"
  ncdump -v bounds_sector ${OUT_FILE} | grep "bounds_sector ="
done
