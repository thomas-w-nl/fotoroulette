#!/bin/bash
echo Installing Fotoroulette
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

# CONFIG
# do not prepend or append directory "/" slashes, unless its the root slash
python_install="/usr/bin/python3"
services_folder="services"

processing_service="fotoroulette_processing.service"
python_file_processing="processing_main.py"


hardware_service="fotoroulette_hardware.service"
python_file_hw="start_server.py HARDWARE"

gui_desktop="fotoroulette_gui.desktop"
python_file_gui="gui_main.py"
gui_logo="assets/images/corendon_logo.png"


# GIFNOC


update_service_file () {
# sed -i '/ExecStart=/c ExecStart=$path_of_executable' $service_file_path
# Update the executable path in a service file to be copied to the systemd folder
sed -i "/ExecStart=/c ExecStart=$1" "$2"
sed -i "/WorkingDirectory=/c WorkingDirectory=$PWD" "$2"
sed -i "/User=/c User=$SUDO_USER" "$2"
}

update_desktop_file () {
# sed -i '/Exec=/c Exec=$path_of_executable' $desktop_file_path
# Update the executable path in a desktop file to be copied to the DE startup folder

sed -i "/Exec=/c Exec=$1" "$2"
sed -i "/Path=/c Path=$PWD/" "$2"
sed -i "/Icon=/c Icon=$PWD/$3" "$2"
}


update_desktop_file "$python_install $PWD/$python_file_gui" "$services_folder/$gui_desktop" "$gui_logo"

update_service_file "$python_install $PWD/$python_file_processing" "$services_folder/$processing_service"
update_service_file "$python_install $PWD/$python_file_hw"  "$services_folder/$hardware_service"

# todo misschien in user space voor startup order? https://wiki.archlinux.org/index.php/Systemd/User#Note_about_X_applications

cp "$services_folder/$processing_service" "/etc/systemd/system/"
cp "$services_folder/$hardware_service" "/etc/systemd/system/"
cp "$services_folder/$gui_desktop" "/home/$SUDO_USER/.config/autostart/"


systemctl enable $processing_service
systemctl enable $hardware_service


systemctl restart $processing_service
systemctl restart $hardware_service

echo Done

