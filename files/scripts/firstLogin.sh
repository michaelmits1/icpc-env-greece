#!/bin/bash
# Close standard output file descriptor
exec 1<&-
# Close standard error file descriptor
exec 2<&-

# Open standard output as $LOG_FILE file for read and write.
exec 1<>/tmp/firstlogin.log
# Redirect standard error to standard output
exec 2>&1


UTILDIR="/icpc"

if [ -f "$UTILDIR/teamWallpaper.png" ]; then
  BACKGROUND="$UTILDIR/teamWallpaper.png"
else
  # Set the wallpaper to the "template"
  BACKGROUND="$UTILDIR/wallpaper.png"
fi

# wait for xfdesktop to be loaded
echo "Waiting for gnome-shell to be running"
while ! pgrep gnome-shell; do
  sleep 1
done

# wait a few moments for things to load initally
sleep 5

#Set the wallpaper for GNOME
if [ -f "$UTILDIR/teamWallpaper.png" ]; then
  BACKGROUND="file://$UTILDIR/teamWallpaper.png"
else
  # Set the wallpaper to the "template"
  BACKGROUND="file://$UTILDIR/wallpaper.png"
fi

gsettings set org.gnome.desktop.background picture-uri "$BACKGROUND"
gsettings set org.gnome.desktop.background picture-uri-dark "$BACKGROUND"
gsettings set org.gnome.desktop.background picture-options 'zoom'

# Reload xfdesktop to get the background image showing (--reload doesn't work, have to --quit first...)
# echo "Reload xfdesktop to refresh the background"
# sleep 5
# xfdesktop --quit
# timeout 5 xfdesktop --reload
# sleep 5
# xfdesktop --quit
# timeout 5 xfdesktop --reload

