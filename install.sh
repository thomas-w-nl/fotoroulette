#!/bin/bash
echo Installing Fotoroulette
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

echo $SUDO_USER

update_service_file () {
# sed -i '/ExecStart=/c ExecStart=$path_of_executable' $service_file_path
# Update the executable path in a service file to be copied to the systemd folder
sed -i "/ExecStart=/c ExecStart=$1" "$2"
sed -i "/WorkingDirectory=/c WorkingDirectory=$PWD" "$2"
sed -i "/User=/c User=$SUDO_USER" "$2"
}


python_install="/home/thomas/PycharmProjects/raspberry-pi/python_install/bin/python3"
services_folder="services"

processing_service="fotoroulette_processing.service"
python_file_processing="processing_main.py"


hardware_service="fotoroulette_hardware.service"
python_file_hw="start_server.py HARDWARE"

update_service_file "$python_install $PWD/$python_file_processing" "$services_folder/$processing_service"
update_service_file "$python_install $PWD/$python_file_hw"  "$services_folder/$hardware_service"

# todo misschien in user space voor startup order? https://wiki.archlinux.org/index.php/Systemd/User#Note_about_X_applications

cp services/fotoroulette* /etc/systemd/system/

systemctl enable $processing_service
systemctl enable $hardware_service


systemctl restart $processing_service
systemctl restart $hardware_service

echo Done

