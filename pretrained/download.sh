#!/bin/bash
ROOTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

CUSTOM_PATH=$1
if [ "$#" -eq 1 ]; then
    outputPath="$CUSTOM_PATH"
else
    outputPath="$ROOTPATH"
fi

if ! [ -x "$(command -v wget)" ]; then
    echo "Error!: wget is not installed! Please install it and try again"
    exit 1
fi

echo -e "\n### ------------------------------------------------------- ###\n"
echo "### Downloading into $outputPath"
echo -e "\n### ------------------------------------------------------- ###\n"

GOOGLE_DRIVE_API_URL="https://docs.google.com/uc?export=download&id="

download_() {
    
    local file_id=$1
    local path=$2
    local file_name=$3
    local internal_url="https://docs.google.com/uc?export=download&id=$file_id"
    local final_url="https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate $internal_url -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=$file_id"
    echo "final_url: $final_url"
    echo -ne "# Downloading "$file_name"\t"
    wget --load-cookies /tmp/cookies.txt $final_url --directory-prefix="$path" -O $file_name && rm -rf /tmp/cookies.txt
    echo -ne "\b\b\b\b"
    echo " # Done"
}

# download_ FILEID PATHDORESULTADO NOMEDOARQUIVO
download_ 1vO_vALz8HXifZaEgtLBvtEq869AKf6kc "$outputPath" "kinetics_tsn_flow.pth.tar"
download_ 1c2z0xrshfpLvhcbkIpNJVcdyPe5rEO-g "$outputPath" "epic_tbn_rgbflowaudio.pth.tar"

echo -e "\n### ------------------------------------------------------- ###\n"
echo "### All Done"
echo -e "\n### ------------------------------------------------------- ###\n"