#!/usr/bin/env bash

for nN in 2 3
do
  for nX in 032 064 128
  do
    fn=Advection1D_SineWaveX1_nN0${nN}_nXC0${nX}_Single
    mpiexec -n 1 ./main1d.gnu.MPI.ex ${fn}.inputs > ${fn}.out
    mkdir ${fn}
    mv ${fn}.inputs ${fn}*out ${fn}
    mv ${fn}*plt00000000* ${fn}/${fn}.init
    mv ${fn}*plt* ${fn}/${fn}.final
  done
done
for nN in 2 3
do
  for nX in 032
  do
    for FC in F T
    do
      fn=Advection1D_SineWaveX1_nN0${nN}_nXC0${nX}_Multi_FC${FC}
      mpiexec -n 1 ./main1d.gnu.MPI.ex ${fn}.inputs > ${fn}.out
      mkdir ${fn}
      mv ${fn}.inputs ${fn}*out ${fn}
      mv ${fn}*plt00000000* ${fn}/${fn}.init
      mv ${fn}*plt* ${fn}/${fn}.final
    done
  done
done
