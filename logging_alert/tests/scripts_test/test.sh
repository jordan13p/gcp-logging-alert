#!/bin/bash

echo "--------------------------------"

curl -i -X GET http://127.0.0.1:8080/healthz \
  -H "Content-Type: application/json"

echo "--------------------------------"

curl -i -X POST http://127.0.0.1:8080/error_log \
  -H "Content-Type: application/json" \
  --data-binary "@pub_sub_data.json"

# echo "--------------------------------"

# curl -i -X POST http://127.0.0.1:8080/counts \
#   -H "Content-Type: application/json" \
#   --data-binary "@pub_sub_data.json"

# echo "--------------------------------"

# curl -i -X POST http://127.0.0.1:8080/counts \
#   -H "Content-Type: application/json" \
#   --data-binary "@pub_sub_data_error.json"

# echo "--------------------------------"

# for ((i=0; i < 7 ; i++)) ; do
#     curl -i -X POST http://127.0.0.1:8080/counts \
#       -H "Content-Type: application/json" \
#       --data-binary "@pub_sub_data.json" &
# done