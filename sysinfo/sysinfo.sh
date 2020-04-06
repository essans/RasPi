#!/bin/bash


#add following line to ~/.bashrc to create an alias
#sysinfo='/home/pi/code/bash/sysinfo.sh'


users=`uptime | grep -o '[0-9]* user[s]' | grep -o '[0-9]*'`

local_wan_ip=`ifconfig wlan0 |grep inet |awk NR==1'{print $2}'`
local_eth_ip=`ifconfig eth0 |grep inet |awk NR==1'{print $2}'`
external_ip=`curl -s ifconfig.me`


soc_temp1=`vcgencmd measure_temp|grep -o "[0-9]*\.[0-9]*"`
soc_temp2=`cat /sys/class/thermal/thermal_zone0/temp`
soc_temp2=`echo "scale=2; $soc_temp2/1000" |bc`

volts_core=`vcgencmd measure_volts core|grep -o "[0-9]*\.[0-9]*"`
volts_sdramc=`vcgencmd measure_volts sdram_c|grep -o "[0-9]*\.[0-9]*"`
volts_sdrami=`vcgencmd measure_volts sdram_i|grep -o "[0-9]*\.[0-9]*"`
volts_sdramp=`vcgencmd measure_volts sdram_p|grep -o "[0-9]*\.[0-9]*"`


mem_free=`free -h | awk 'NR==2{print \$4}'`

mem_arm=`vcgencmd get_mem arm|grep -o "[0-9]*[A-Z]*"`
mem_gpu=`vcgencmd get_mem gpu|grep -o "[0-9]*[A-Z]*"`

throttled_status=`vcgencmd get_throttled |grep -o "[0-9]*x[0-9]*"`

m1_load_avg=`uptime | grep -o 'load average[s:][: ].*'| awk '{print \$3}' | tr -d ','`
m5_load_avg=`uptime | grep -o 'load average[s:][: ].*'| awk '{print \$4}' | tr -d ','`
m15_load_avg=`uptime | grep -o 'load average[s:][: ].*'| awk '{print \$5}'`


datetime=`date +%Y-%m-%d\ %T`
up_since=`uptime -s`

echo ' '
echo '============================================='
echo 'SYSTEM_INFORMATION'
echo '============================================='

echo ' '

printf "%-25s %-15s\n" "users" "$users"

echo ' '

printf "%-25s %-15s\n" "local_wan_ip" "$local_wan_ip"
printf "%-25s %-15s\n" "local_eth_ip" "$local_eth_ip"
printf "%-25s %-15s\n" "external_ip" "$external_ip"

echo ' '

printf "%-25s %-15s\n" "dateTime" "$datetime"
printf "%-25s %-15s\n" "up_since" "$up_since"

echo ' '

printf "%-25s %-15s\n" "SoC_temp" "$soc_temp1" #system-on-chip temperature
printf "%-25s %-15s\n" "SoC_temp2" "$soc_temp2"  #ditto

echo ' '

printf "%-25s %-15s\n" "1m_load_avg" "$m1_load_avg"
printf "%-25s %-15s\n" "5m_load_avg" "$m5_load_avg"
printf "%-25s %-15s\n" "15m_load_avg" "$m15_load_avg"


echo ' '

printf "%-25s %-15s\n" "volts_core" "$volts_core" #GPU processor core
printf "%-25s %-15s\n" "volts_SDRAM_controller" "$volts_sdramc" #SDRAM controller
printf "%-25s %-15s\n" "volts_SDRAM_IO" "$volts_sdrami" #SDRAM input/output
printf "%-25s %-15s\n" "volts_SDRAM_phyMem" "$volts_sdramp" #SDRAM physical memory

echo ' '

printf "%-25s %-15s\n" "free_mem" "$mem_free" #free memory from free -h

echo ' '

printf "%-25s %-15s\n" "cpu_allocMem" "$mem_arm" #cpu allocated memory
printf "%-25s %-15s\n" "gpu_allocMem" "$mem_gpu" #gpu allocated memory

echo ' '

printf "%-25s %-15s\n" "throttled_status=$throttled_status"

echo ' '

echo '============================================='

echo ' '
