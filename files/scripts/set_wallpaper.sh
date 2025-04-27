#!/bin/bash

# Set the wallpaper for GNOME
gsettings set org.gnome.desktop.background picture-uri "file:///icpc/wallpaper.png"
gsettings set org.gnome.desktop.background picture-uri-dark "file:///icpc/wallpaper.png"
gsettings set org.gnome.desktop.background picture-options 'zoom'

# If using older GNOME that doesn't support dark mode URIs
if ! gsettings get org.gnome.desktop.background picture-uri-dark &>/dev/null; then
  echo "This version of GNOME doesn't support dark mode wallpaper"
fi

echo "ze wallpaper has been added successfully"