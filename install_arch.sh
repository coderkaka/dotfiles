#!/bin/sh
#Mount root fs to /mnt
#首先格式化硬盘，并挂载硬盘分区到/mnt，然后执行 sh install_arch.sh
function genAutoPasswd(){
    #change user password
    cat > /mnt/root/passwd.sh << EOF
    #!/usr/bin/expect
    set username [lindex \$argv 0]
    spawn passwd \$username
    expect "New password:"
    send "zhangqiong\n"
    expect "Retype new password:"
    send "zhangqiong\n"
    expect eof
EOF
}

function genFirstBootService(){
    #Setting boot service
    #must generate in chroot
    cat > /mnt/etc/systemd/system/firstboot.service << EOF
    [Unit]
    Description=First Boot
    After=dhcpcd.service
    Requires=dhcpcd.service
    [Service]
    ExecStart=/bin/bash /root/firstboot.sh > /root/install.log 2&>1
    [Install]
    WantedBy=multi-user.target
EOF
}

function genSettingFile(){
    cat > /mnt/root/setting.sh << ST_END
    #Configure the install according to official guide and will execute in target system.

    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 
    hwclock --systohc
    sed -i  '/#zh_CN\.UTF-8 UTF-8/{s/^#//;}' /etc/locale.gen
    sed -i  '/#en_US\.UTF-8 UTF-8/{s/^#//;}' /etc/locale.gen
    locale-gen
    echo "LANG=en_US.UTF-8" > /etc/locale.conf
    echo "coderkaka" >/etc/hostname

    #config host
    echo "127.0.0.1 localhost.localdomain localhost
    ::1 localhost.localdomain localhost
    127.0.1.1 coderkaka.localdomain coderkaka" > /etc/hosts
 
    expect /root/passwd.sh root
    useradd coderkaka
    mkdir /home/coderkaka
    chown coderkaka:coderkaka /home/coderkaka -R
    expect /root/passwd.sh coderkaka

    systemctl enable dhcpcd.service 
    systemctl enable firstboot.service 

    #grub-install --target=x86_64-efi --efi-directory=/boot/ --bootloader-id=boot
    grub-mkconfig -o /boot/grub/grub.cfg

ST_END

}


function genAdvanceSetting(){
   cat > /mnt/root/00-keyboard.conf << KB
    Section "InputClass"
        Identifier "system-keyboard"
        MatchIsKeyboard "on"
        Option "XkbLayout" "us"
        Option "XkbModel" "pc105"
   EndSection
KB

    cat >/mnt/root/10-monitor.conf << MONITOR
    Section "Monitor"                                           
    Identifier  "eDP1"
    Option      "Primary" "true"
    EndSection
 
    Section "Monitor"
    Identifier  "HDMI1"
    Option      "Above" "eDP1"
    EndSection
MONITOR

    cat >/mnt/root/20-natural-scrolling.conf << NAT
    Section "InputClass"
        Identifier "libinput pointer catchall"
        MatchIsPointer "on"                                 
        MatchDevicePath "/dev/input/event*"
        Driver "libinput"
        Option "NaturalScrolling" "true"
    EndSection
 
    Section "InputClass"
        Identifier "libinput touchpad catchall"
        MatchIsTouchpad "on"
        MatchDevicePath "/dev/input/event*"
        Driver "libinput"
        Option "NaturalScrolling" "true"
    EndSection
NAT

    cat > /mnt/root/30-touchpad.conf << TP
   Section "InputClass"                                        
        Identifier "MyTouchpad"
        MatchIsTouchpad "on"
        Driver "libinput"
        Option "Tapping" "on"
    EndSection

TP

}

function genInstallScript(){
    #firstboot.sh will execute in target system in the firstboot. And first boot will install other packages.
    cat > /mnt/root/firstboot.sh << INSTALL

    #Generate pacman configure
    #Config mirror
    sed -i '/^[^#]/{s/^/#/}' /etc/pacman.d/mirrorlist
    sed -i '/https.*ustc.*/{s/^#//}' /etc/pacman.d/mirrorlist
    cat >> /etc/pacman.conf << MIRROR
    [archlinuxfr]
    SigLevel = Never
    Server=http://repo.archlinux.fr/\\\$arch

    [archlinuxcn]
    SigLevel = Optional TrustAll
    Server=http://mirrors.ustc.edu.cn/archlinuxcn/\\\$arch
MIRROR

    #登录网关，并测试网络，直到畅通
    curl -d "DDDDD=2012211529" -d "upass=zq1993" -d "0MKKey=" http://10.3.8.211 2>&1 > /dev/null 2>&1
    ping -c 2 -W 2 baidu.com
    while ((\$?!=0))
    do
        curl -d "DDDDD=2012211529" -d "upass=zq1993" -d "0MKKey=" http://10.3.8.211 2>&1 > /dev/null 2>&1
        sleep 2
        ping -c 2 -W 2 baidu.com
    done

    PFLAG="-S --noconfirm --needed"
    pacman -Syy
    pacman \$PFLAG yaourt
    if [ \$? -ne 0 ];then
        exit
    fi

    #drivers 
    pacman \$PFLAG xf86-video-intel xf86-video-vesa xf86-input-keyboard xf86-input-mouse xf86-input-libinput xf86-input-vmmouse xf86-input-void xf86-video-fbdev   nvidia bumblebee

    #xorg drivers
    pacman \$PFLAG xterm xorg-bdftopcf xorg-docs xorg-fonts-100dpi xorg-fonts-75dpi xorg-fonts-encodings xorg-font-util xorg-luit xorg-mkfontdir xorg-mkfontscale xorg-server xorg-server-common xorg-setxkbmap xorg-xauth xorg-xbacklight xorg-xev xorg-xhost xorg-xinit xorg-xinput xorg-xkbcomp xorg-xkbevd xorg-xkbutils xorg-xlsclients xorg-xmodmap xorg-xprop xorg-xrandr xorg-xrdb

    #networks
    pacman \$PFLAG network-manager-applet networkmanager nethogs ntp openssh tcpdump transmission-cli transmission-qt 
    #audio and video 

    pacman \$PFLAG pulseaudio pulseaudio-alsa pulseaudio-bluetooth alsa-utils ffmpeg gstreamer smplayer netease-cloud-music 

    #bluetooth
    pacman \$PFLAG bluez bluez-firmware bluez-utils


    #little tool
    pacman \$PFLAG xfce4-terminal tmux zathura zathura-pdf-poppler you-get xdiskusage wget unzip unrar udevil tsocks tree strace sdcv rsync fsarchiver redis hiredis progress powertop pcmanfm parted oprofile ntfs-3g nmap lynx lsof lftp kexec-tools iotop htop gpicview gparted gptfdisk dos2unix dosfstools  foremost dmidecode wps-office smartmontools scrot 

    #program tool
    pacman \$PFLAG gcc gdb ctags cscope clang emacs git go google-chrome jdk8-openjdk python python2 python2-pip python-pip  qemu ruby scala sublime-text valgrind zsh docker android-udev

    #font 
    pacman \$PFLAG powerline-fonts ttf-liberation ttf-monaco ttf-wps-fonts wqy-microhei wqy-microhei-lite

    #input
    pacman \$PFLAG fcitx fcitx-configtool fcitx-gtk2 fcitx-gtk3  vim-fcitx  


    #wm
    pacman \$PFLAG i3-wm lxdm dmenu i3lock i3status unclutter compton 

    pip install i3pystatus colour netifaces shadowsocks


    pacman \$PFLAG abs
    pacman \$PFLAG intel-ucode grub2-theme-arch-leap  


    chsh -s /usr/bin/zsh coderkaka
    chsh -s /usr/bin/zsh root
    gpasswd -a coderkaka wheel
    gpasswd -a coderkaka bumblebee
    chmod 777 /etc/sudoers
    sed -i '/NOPASSWD/{s/^# *//}' /etc/sudoers
    chmod 0440 /etc/sudoers

    su - coderkaka -c "yaourt \$PFLAG archlinux-lxdm-theme i3lock-wrapper setroot ttf-ms-fonts"

    systemctl enable dhcpcd.service 
    systemctl enable lxdm.service
    systemctl enable NetworkManager.service
    systemctl disable firstboot.service

    cp /usr/share/tsocks/tsocks.conf.complex.example /etc/tsocks.conf
    sed -i '/Industrial/{s/Industrial/Archlinux/g}' /etc/lxdm/lxdm.conf
    sed -i '/Industrial/{s/Industrial/Archlinux/g}' /etc/lxdm/lxdm.conf
    sed -i '/keyboard/{s/udev/udev resume/g}' /etc/mkinitcpio.conf
    mkinitcpio -p linux

    fallocate -l 4G /swap
    chmod 600 /swap
    mkswap /swap
    swapon /swap
    echo "/swap none swap defaults 0 0" >> /etc/fstab

    resume=\$(sed -n '/\/[^[:alnum:]]/p' /etc/fstab |awk '{print \$1}'| cut -d = -f 2)
    resume_offset=\$(filefrag -v /swap | head -4|tail -1 |awk '{print \$5}'| sed -n 's/[^[:alnum:]]//p')

    sed -i '/GRUB_TERMINAL_OUTPUT/{s/^#//}' /etc/default/grub
    sed -i "/quiet/{s/quiet/quiet resume=UUID="\$resume" resume_offset="\$resume_offset"/}" /etc/default/grub

    grub-mkconfig -o /boot/grub/grub.cfg
    mv /root/*.conf /etc/X11/xorg.conf.d/

    reboot
INSTALL

}

#Beginning to Execute
#Execute in Host system  and install base target system
#在/mnt中安装基础系统
pacstrap /mnt base base-devel vim expect efibootmgr grub dialog
if [ $? -ne 0 ] ;then 
    exit
fi

#生成文件系统配置文件
genfstab -U  /mnt >> /mnt/etc/fstab

#cp -r /home/coderkaka/.[^.]* /mnt/home/coderkaka/
#生成自动设置密码文件passwd.sh
genAutoPasswd
#生成第一次启动的systemd service文件firstboot.service
genFirstBootService

#生成在chroot下执行的配置（包括时区等）文件setting.sh
#The first two function must execute in prior;
genSettingFile 

#执行生成的配置脚本,完成基本系统的初始化任务
arch-chroot /mnt bash /root/setting.sh

#生成提前的配置文件
#如xorg的一些配置文件等,这些文件没有模板，因此手动生成
#有模板的，只需要修改一些部分的配置文件都在安装脚本firstboot.sh中完成
genAdvanceSetting

#生成系统启动后第一次执行的安装脚本 firstboot.sh
genInstallScript

#1.配置vim .vimrc .vim https://github.com/tao12345666333/vim/blob/master/vimrc
#2.配置zsh .zshrc .oh-my-zsh  https://github.com/robbyrussell/oh-my-zsh
#3.配置xfce4-terminal .config/xfce4/terminal .config/dircolors https://github.com/seebi/dircolors-solarized
#4.配置sdcv .stardict/ .config/startdict
#5.配置chrome
#6.配置lxdm .dmrc
#7.配置键盘键位 .Xmodmap
#8.配置git .gitconfig
#9. .Xmodmap .xprofile 
#10. i3 .config/i3/
#11. shadowsocks .config/shadowsocks
grub-mkconfig -o /boot/grub/grub.cfg
#reboot
