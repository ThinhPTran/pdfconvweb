#!/bin/bash

# Input: source file path and destination folder
SOURCE_FILE=$1
DEST_FOLDER=$2

# Get the filename and extension
FILENAME=$(basename "$SOURCE_FILE")
NAME="${FILENAME%.*}"
EXT="${FILENAME##*.}"

# Create the new filename
NEW_FILENAME="${NAME}_converted.${EXT}"

# Move and rename the file
ocrmypdf "$SOURCE_FILE" "$DEST_FOLDER/$NEW_FILENAME"
