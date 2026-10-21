#!/bin/bash
# gsplat source build for the splat venv, RAM-guarded.
# MAX_JOBS=2 + watchdog: if MemAvailable < 700MB, kill build processes.
set -u
VENV=$HOME/venvs/splat
CUDA=$HOME/opt/cuda/usr/local/cuda-13.2
TC=$HOME/opt/toolchain/usr
LOG=$HOME/work/build/gsplat-build.log

export CUDA_HOME=$CUDA
export PATH=$CUDA/bin:$TC/bin:$PATH
export LD_LIBRARY_PATH=$TC/lib/aarch64-linux-gnu:$CUDA/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
# Toolchain g++-13 as CC too: nvcc -ccbin follows CC and needs cc1plus,
# which the system gcc lacks (no system g++).
export CC=$TC/bin/g++-13
export CXX=$TC/bin/g++-13
export CUDAHOSTCXX=$TC/bin/g++-13
export TORCH_CUDA_ARCH_LIST="8.7"
export MAX_JOBS=1  # 2 parallel nvcc jobs OOM'd (watchdog kill at 428MB avail); desktop needs ~3.2GB
export CPATH=$HOME/opt/pydev/usr/include/python3.12:$HOME/opt/pydev/usr/include${CPATH:+:$CPATH}  # Python.h + arch pyconfig.h (no python-dev on box)
export TORCH_EXTENSIONS_DIR=$HOME/work/build/torch-ext

source $VENV/bin/activate
cd $HOME/work/build/gsplat-src

# watchdog: kill compilers if memory gets truly dire (2s poll; the peak
# single nvcc job legitimately dips avail to ~600MB, so the floor is 350MB)
(
  while :; do
    avail=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
    if [ "${avail:-9999}" -lt 350 ]; then
      echo "$(date -u +%H:%M:%S) WATCHDOG: MemAvailable ${avail}MB < 350MB, killing build" >> $LOG
      pkill -9 -f 'cudafe|cicc|nvcc|cc1plus|ninja|ptxas' 2>/dev/null
      exit 33
    fi
    sleep 2
  done
) &
WD=$!

# a peak single-file compile needs ~3.6GB; wait for headroom instead of
# dying mid-file when the desktop is heavy
while :; do
  avail=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
  [ "$avail" -ge 4300 ] && break
  echo "$(date -u +%H:%M:%S) waiting for memory: ${avail}MB avail < 4300MB" >> $LOG
  sleep 120
done

echo "$(date -u) build start: pip install -e gsplat-src (MAX_JOBS=$MAX_JOBS arch=8.7)" >> $LOG

nice -n 19 pip install -e . --no-build-isolation -v >> $LOG 2>&1
rc=$?
kill $WD 2>/dev/null
echo "$(date -u) build end rc=$rc" >> $LOG
exit $rc
