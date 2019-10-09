#!/bin/bash                     
ulimit -c unlimited
nohup setsid ./addr.py >&addr.log &
cd ..
