#!/bin/bash
source /workspace/mobinha_license/src/morai_ws/devel/setup.bash
export PYTHONPATH=$PYTHONPATH:/workspace/mobinha_license/src/mobinha/
python3 ../car/car.py &
python3 ../control/control.py &
python3 ../planning/planning.py &
python3 ../perception/perception.py 
