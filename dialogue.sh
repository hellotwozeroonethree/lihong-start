#!/bin/bash

dialog --title Testing --msgbox "Error" 10 20

dialog --textbox /etc/passwd 15 45
# textbox only include file text, no input line text
echo -e "\n"
echo "***********************************"
echo "Finished"
