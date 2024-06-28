#!/bin/bash
# run the python function to write the torrent link in a txt file
python3 ~/nextcloud/bash_stuff/scripts/downloading_movies/magnetLink.py 0

# Remote server details
remote_user="gerard"
remote_server="186.154.6.93" #"192.168.0.145"
remote_port="24"

# Path to the text file containing the magnet link
text_file="$HOME/nextcloud/bash_stuff/scripts/downloading_movies/magnet_link.txt"

#Check if the file exists
if [ ! -f "$text_file" ]; then
    echo "Error: Text file not found."
    exit 1
fi

# Get the first line from the text file
magnet_link=$(head -n 1 "$text_file")

# Check if the magnet link is empty
if [ -z "$magnet_link" ]; then
    echo "Error: Magnet link not found in the file."
    exit 1
fi

# Run the transmission-remote command on the remote server via ssh
#ssh "$remote_user@$remote_server" "transmission-remote --auth gerard:naranja8712 -a \"$magnet_link\""

#ssh "$remote_user@$remote_server -p $remote_port" "transmission-remote --auth gerard:naranja8712 -a \"$magnet_link\""
# Run the transmission-remote command on the remote server via ssh
ssh -p "$remote_port" "$remote_user@$remote_server" "transmission-remote --auth gerard:naranja8712 -a \"$magnet_link\""
