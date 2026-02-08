#!/bin/bash
#
#
if [[ $# -lt 1 ]] || [[ ! -d $1   ]]; then
	echo "Usage:
	$0 <dir containg images>"
	exit 1
fi

WALLPAPER=$(find "$1" -type f -print0 | shuf -zn1 | xargs -0)


awww img "$WALLPAPER"
rm ~/Pictures/current_wallpaper
ln -s "$WALLPAPER" ~/Pictures/current_wallpaper
matugen image "$WALLPAPER"
 
