#!/bin/sh

mkdir data
mkdir data/extracted
mkdir data/cache
mkdir data/compressed
mkdir user
cp example_config.json user/config.json
curl 'https://download.wetransfer.com/eugv/df3769d9f6937b74c7163ad81b4ab71a20221107214454/8393cf071de8a65b3c5a212e1fcd57994cab0d3e/rotten_tomatoes.zip?token=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2Njc4NTc1NDEsImV4cCI6MTY2Nzg1ODE0MSwidW5pcXVlIjoiZGYzNzY5ZDlmNjkzN2I3NGM3MTYzYWQ4MWI0YWI3MWEyMDIyMTEwNzIxNDQ1NCIsImZp' --location --output data/compressed/rotten_tomatoes.zip
unzip data/compressed/rotten_tomatoes.zip
mv rotten_tomatoes*.csv data/extracted
