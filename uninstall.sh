#!/bin/bash
echo Installing Fotoroulette
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

# CONFIG
# do not prepend or append directory "/" slashes, unless its the root slash
processing_service="fotoroulette_processing.service"
hardware_service="fotoroulette_hardware.service"
gui_desktop="fotoroulette_gui.desktop"
# GIFNOC

systemctl stop $processing_service
systemctl stop $hardware_service

systemctl disable $processing_service
systemctl disable $hardware_service

rm "/etc/systemd/system/$processing_service"
rm "/etc/systemd/system/$hardware_service"
rm "/home/$SUDO_USER/.config/autostart/$gui_desktop"

echo Done

