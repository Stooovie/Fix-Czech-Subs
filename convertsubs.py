#!/usr/bin/env python3

import os
import chardet
import shutil

def clean_and_decode(raw_data):
    """Attempt to clean and decode the raw data."""
    try:
        # Try to decode as UTF-8 first
        return raw_data.decode('utf-8')
    except UnicodeDecodeError:
        # If UTF-8 fails, try to clean the data and decode
        cleaned = raw_data.replace(b'\x00', b'')  # Remove null bytes
        try:
            return cleaned.decode('utf-8')
        except UnicodeDecodeError:
            return None

def convert_to_utf8(file_path):
    """
    Attempt to convert the subtitle file to UTF-8, backup the original, and overwrite it.
    """
    encodings_to_try = ['utf-8', 'windows-1250', 'iso-8859-2', 'cp1252']
    
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    
    # Try chardet first
    detected_encoding = chardet.detect(raw_data)['encoding']
    if detected_encoding and detected_encoding not in encodings_to_try:
        encodings_to_try.insert(0, detected_encoding)
    
    # Try decoding with different encodings
    for encoding in encodings_to_try:
        try:
            decoded_data = raw_data.decode(encoding)
            print(f"Successfully decoded {file_path} using {encoding}")
            break
        except UnicodeDecodeError:
            continue
    else:
        # If all encodings fail, try cleaning the data
        decoded_data = clean_and_decode(raw_data)
        if decoded_data is None:
            print(f"Error decoding {file_path}. Skipping this file.")
            return

    # Create a backup of the original file
    backup_file = file_path + ".bkp"
    shutil.copy2(file_path, backup_file)
    
    # Overwrite the original file with UTF-8 encoded content
    with open(file_path, 'w', encoding='utf-8') as utf8_file:
        utf8_file.write(decoded_data)
    
    print(f"Converted {file_path} to UTF-8 and overwritten. Backup created: {backup_file}")

def scan_directory(directory):
    """
    Scan a directory for subtitle files with 'cs' in the filename and convert them to UTF-8.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if 'cs' in file.lower() and file.endswith(('.srt', '.sub', '.txt')):
                file_path = os.path.join(root, file)
                convert_to_utf8(file_path)


# Specify the directory containing subtitle files
directory_to_scan = "/Volumes/Public/Video/Movies"
scan_directory(directory_to_scan)
