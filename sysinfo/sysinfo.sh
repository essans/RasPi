#!/bin/bash


#add following line to ~/.bashrc to create an alias
#sysinfo='/home/pi/code/bash/sysinfo.sh'

#can also auto-run via crontab -e and dump to a file
#0,15,30,45 * * * * bash /home/pi/code/bash/sysinfo.sh > /home/pi/log/$(uname -n)_sysinfo.dump


users=`uptime | grep -o '[0-9]* user[s]' | grep -o '[0-9]*'`

local_wan_ip=`/sbin/ifconfig wlan0 |grep inet |awk NR==1'{print $2}'`
local_eth_ip=`/sbin/ifconfig eth0 |grep inet |awk NR==1'{print $2}'`
external_ip=`curl -s ifconfig.me`


soc_temp1=`vcgencmd measure_temp|grep -o "[0-9]*\.[0-9]*"`
soc_temp2=`cat /sys/class/thermal/thermal_zone0/temp`
soc_temp2=`echo "scale=2; $soc_temp2/1000" |bc`
pmic_temp=`vcgencmd measure_temp pmic | grep -o "[0-9]*\.[0-9]*"`

cpu_idle=`top -b -n 1 | sed -n "s/^%Cpu.*ni, \([0-9.]*\) .*$/\1/p"`


volts_core=`vcgencmd measure_volts core|grep -o "[0-9]*\.[0-9]*"`
volts_sdramc=`vcgencmd measure_volts sdram_c|grep -o "[0-9]*\.[0-9]*"`
volts_sdrami=`vcgencmd measure_volts sdram_i|grep -o "[0-9]*\.[0-9]*"`
volts_sdramp=`vcgencmd measure_volts sdram_p|grep -o "[0-9]*\.[0-9]*"`

filesys_free=`df -B M / | awk NR==2'{print $4}' | grep -o "[0-9]*"`

mem_free=`free -m | awk 'NR==2{print \$4}'`
swap_free=`free -m |awk 'NR==3{print \$4}'` #can be set in /etc/dphys-swapfile


#mem_arm=`vcgencmd get_mem arm|grep -o "[0-9]*[A-Z]*"`  #does not work of raspi4
mem_gpu=`vcgencmd get_mem gpu|grep -o "[0-9]*[A-Z]*"` #set via sudo raspi-config
mem_gpu_malloc_total=`vcgencmd get_mem malloc_total | grep -o "[0-9]*[A-Z]*"` # total memory assigned to gpu malloc heap
mem_gpu_malloc_free=`vcgencmd get_mem malloc | grep -o "[0-9]*[A-Z]*"` # free  memory in  gpu malloc heap
mem_gpu_reloc_total=`vcgencmd get_mem reloc_total | grep -o "[0-9]*[A-Z]*"` # total memory assigned to gpu relocatable heap
mem_gpu_reloc_free=`vcgencmd get_mem reloc | grep -o "[0-9]*[A-Z]*"` # free gpu memory in relocatale heap


clock_arm=`vcgencmd measure_clock arm | grep -o "=.*" | cut -d"=" -f2`
clock_arm_mhz=`echo "scale=1; $clock_arm/1000000" |bc`

clock_core=`vcgencmd measure_clock core | grep -o "=.*" | cut -d"=" -f2`
clock_core_mhz=`echo "scale=1; $clock_core/1000000" |bc`

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

printf "%-25s %-15s\n" "dateTime" "$datetime"
printf "%-25s %-15s\n" "up_since" "$up_since"

echo ' '

printf "%-25s %-15s\n" "users" "$users"

echo ' '

printf "%-25s %-15s\n" "local_wan_ip" "$local_wan_ip"
printf "%-25s %-15s\n" "local_eth_ip" "$local_eth_ip"
printf "%-25s %-15s\n" "external_ip" "$external_ip"

echo ' '

printf "%-25s %-15s\n" "SoC_temp1" "$soc_temp1" #system-on-chip temperature
printf "%-25s %-15s\n" "SoC_temp2" "$soc_temp2"  #ditto


printf "%-25s %-15s\n" "pmic_temp" "$pmic_temp" #pmic temperature

echo ' '

printf "%-25s %-15s\n" "cpu_idle" "$cpu_idle"


echo ' '

printf "%-25s %-15s\n" "1m_load_avg" "$m1_load_avg"
printf "%-25s %-15s\n" "5m_load_avg" "$m5_load_avg"
printf "%-25s %-15s\n" "15m_load_avg" "$m15_load_avg"

echo ' '

printf "%-25s %-15s\n" "volts_core" "$volts_core" #GPU processor core
printf "%-25s %-15s\n" "volts_SDRAM_ctrlr" "$volts_sdramc" #SDRAM controller
printf "%-25s %-15s\n" "volts_SDRAM_IO" "$volts_sdrami" #SDRAM input/output
printf "%-25s %-15s\n" "volts_SDRAM_phyMem" "$volts_sdramp" #SDRAM physical memory

echo ' '

printf "%-25s %-15s\n" "clock_arm_mhz" "$clock_arm_mhz"
printf "%-25s %-15s\n" "clock_core_mhz" "$clock_core_mhz"


echo ' '

printf "%-25s %-15s\n" "file_sys_free" "$filesys_free" 

echo ' '

printf "%-25s %-15s\n" "mem_free" "$mem_free" 
printf "%-25s %-15s\n" "swap_free" "$swap_free"


echo ' '

#printf "%-25s %-15s\n" "cpu_allocMem" "$mem_arm" #cpu allocated memory
printf "%-25s %-15s\n" "gpu_allocMem" "$mem_gpu" #gpu allocated memory
printf "%-25s %-15s\n" "gpu_mallocTotal" "$mem_gpu_malloc_total" #gpu allocated memory
printf "%-25s %-15s\n" "gpu_mallocFree" "$mem_gpu_malloc_free"
printf "%-25s %-15s\n" "gpu_relocTotal" "$mem_gpu_reloc_total" 
printf "%-25s %-15s\n" "gpu_relocFree" "$mem_gpu_malloc_free"

echo ' '

printf "%-25s %-15s\n" "throttled_status" "$throttled_status"

echo ' '

echo '============================================='

echo ' '
