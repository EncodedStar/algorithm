#!/bin/bash                     
ulimit -c unlimited
nohup setsid ./echo.py >&echo.log &
cd ..
