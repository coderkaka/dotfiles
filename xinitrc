
#!/bin/sh

#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)
#
export XIM_PROGRAM=fcix
export XIM=fcitx
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS="@im=fcitx"

export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

#ping -w 1 -c 1 10.3.9.5
#if [ $? -eq 0 ]; then
#    echo "haha"
#    /usr/sbin/ntpdate -u 10.3.9.5
#fi
if [ ! -d /dev/shm/.cache ]; then
    mkdir /dev/shm/.cache
    mkdir -p /dev/shm/.cache/netease-cloud-music/Cef/
    ln -sv ~/.config/netease-cloud-music/Cache /dev/shm/.cache/netease-cloud-music/Cef/
fi

if [ -f $HOME/.Xmodmap ]; then
    /usr/bin/xmodmap $HOME/.Xmodmap
fi

exec i3
#DEFAULT_SESSION=xfce4-session
#DEFAULT_SESSION=i3
#case $1 in
#  xfce) exec dbus-launch xfce4-session ;;
#  *) exec dbus-launch  $DEFAULT_SESSION ;;
#esac
#
