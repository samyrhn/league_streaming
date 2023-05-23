#!/bin/bash
set -e

# Remove 'app/packages' directory and 'app.zip' file if they exist
rm -rf app/packages app.zip

# Change directory to 'app'
cd app/

# Install packages specified in 'requirements.txt' to './packages'
pip install --target ./packages -r requirements.txt

# Change directory to 'packages'
cd packages

# Zip all files and directories in 'packages' into '../app.zip'
zip -r ../app.zip .

# Go up a directory
cd ..

# Zip specified directories and file into 'app.zip'
zip -r app.zip kafka_producer/ riot_api/ lambda_function.py

# Update AWS lambda function code
aws lambda update-function-code --function-name LambdaFunctionLeagueStreaming --zip-file fileb://app.zip

