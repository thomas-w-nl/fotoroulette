#!/bin/bash
echo Installing Fotoroulette
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

update_service_file () {
# sed -i '/ExecStart=/c ExecStart=$path_of_executable' $service_file_path
# Update the executable path in a service file to be copied to the systemd folder
sed -i "/ExecStart=/c ExecStart=$1" "$2"
}

services_folder="services"

processing_service="fotoroulette_processing.service"
python_file_processing="python3 $PWD/processing_main.py"
update_service_file "$python_file_processing" "$services_folder/$processing_service"


gui_service="fotoroulette_gui.service"
python_file_gui="python3 $PWD/gui_main.py"
update_service_file "$python_file_gui"  "$services_folder/$gui_service"


hardware_service="fotoroulette_hardware.service"
python_file_hw="python3 $PWD/start_server.py"
update_service_file "$python_file_hw"  "$services_folder/$hardware_service"

# todo misschien in user space voor startup order? https://wiki.archlinux.org/index.php/Systemd/User#Note_about_X_applications

cp services/fotoroulette* /etc/systemd/system/

systemctl enable $processing_service
systemctl enable $gui_service
systemctl enable $hardware_service

echo Done

