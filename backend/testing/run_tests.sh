#!/bin/bash

# start flask API in BG, sending stderr and stdout to /dev/null
python3 ../main.py -t > /dev/null 2>&1 &

# wait for API to start running
sleep 10

# run tests
python3 test_api_iot.py

# shutdown by special route
curl localhost:8080/shutdown






