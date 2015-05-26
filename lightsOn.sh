#!/bin/bash
# lightsOn.sh
#set -x

# Copyright (c) 2013 iye.cba at gmail com
# url: https://github.com/iye/lightsOn
# This script is licensed under GNU GPL version 2.0 or above

# Modified by Stephane HUC
# year: 2015 >
# url: https://github.com/hucste/lightsOn
# email: devs@stephane-huc.net

# Description: Bash script that prevents the screensaver and display power
# management (DPMS) to be activated when you are watching Flash Videos
# fullscreen on Firefox and Chromium.
# Can detect mplayer, minitube, and VLC when they are fullscreen too.
# Also, screensaver can be prevented when certain specified programs are running.
# lightsOn.sh needs xscreensaver or kscreensaver to work.


# HOW TO USE: Start the script with the number of seconds you want the checks
# for fullscreen to be done. Example:
# "./lightsOn.sh 120 &" will Check every 120 seconds if Mplayer, Minitube
# VLC, Firefox or Chromium are fullscreen and delay screensaver and Power Management if so.
# You want the number of seconds to be ~10 seconds less than the time it takes
# your screensaver or Power Management to activate.
# If you don't pass an argument, the checks are done every 50 seconds.
#
# An optional array variable exists here to add the names of programs that will delay the screensaver if they're running.
# This can be useful if you want to maintain a view of the program from a distance, like a music playlist for DJing,
# or if the screensaver eats up CPU that chops into any background processes you have running,
# such as realtime music programs like Ardour in MIDI keyboard mode.
# If you use this feature, make sure you use the name of the binary of the program (which may exist, for instance, in /usr/bin).
clear

# Modify these variables if you want this script to detect if Mplayer,
# VLC, Minitube, or Firefox or Chromium Flash Video are Fullscreen and disable
# xscreensaver/kscreensaver and PowerManagement.

declare -a APPS=("chromium" "firefox" "google-chrome" "opera")
APPS=("${APPS[@]}" "gnome-mplayer" "mplayer" "mplayer2" "mpv" "smplayer" "totem" "vlc")
APPS=("${APPS[@]}" "minitube" "popcorn-time" "smtube")

# Names of programs which, when running, you wish to delay the screensaver.
delay_progs=() # For example ('ardour2' 'gmpc')

# Screensavers Names Software
declare -a screensavers=("cinnamon-screensaver" "gnome-screensaver" "kscreensaver" "xautolock" "xscreensaver")

# YOU SHOULD NOT NEED TO MODIFY ANYTHING BELOW THIS LINE
delay="$1"
displays=""

LOCKFILE="/var/run/lock/$(basename $0)" ;
#pwd="$(cd "$(dirname "$0")" && pwd)"
pwd="$(dirname $(readlink -f $0))"

function checkDelayProgs() {
    for prog in "${delay_progs[@]}"; do
        if [[ $(pidof "${prog}") -ge 1 ]]; then
            echo "Delaying the screensaver because a program on the delay list, '${prog}', is running..."
            delayScreensaver
            break
        fi
    done
}

function checkFullscreen() {
    # loop through every display looking for a fullscreen window
    for display in $displays
    do
        #get id of active window and clean output
        activ_win_id="$(DISPLAY=:0.${display} xprop -root _NET_ACTIVE_WINDOW)"
        #activ_win_id=${activ_win_id#*# } #gives error if xprop returns extra ", 0x0" (happens on some distros)
        activ_win_id=${activ_win_id:40:9}

        # Skip invalid window ids (commented as I could not reproduce a case
        # where invalid id was returned, plus if id invalid
        # isActivWinFullscreen will fail anyway.)
        #if [ "$activ_win_id" = "0x0" ]; then
        #     continue
        #fi

        if [[ -n $activ_win_id ]]; then
            # Check if Active Window (the foremost window) is in fullscreen state
            isActivWinFullscreen="$(DISPLAY=:0.${display} xprop -id ${activ_win_id} | grep _NET_WM_STATE_FULLSCREEN)"
            if [[ "${isActivWinFullscreen}" = *NET_WM_STATE_FULLSCREEN* ]]; then
                if isAppRunning; then delayScreensaver; fi
            else
                xset dpms
            fi
        fi

    done
}

function detect_id_displays() {
    # enumerate all the attached screens

    #while read id; do
        #displays="${displays} ${id}"
    #done < <(xvinfo | sed -n 's/^screen #\([0-9]\+\)$/\1/p')

    displays=$(xvinfo | awk -F'#' '/^screen/ {print $2}' | xargs)
}

function detect_screensaver_used() {
    # Detect screensaver been used

    for saver in "${screensavers[@]}"; do
        if [[ -n $(pidof "${saver}") ]]; then screensaver="${saver}"; fi
    done

    if [[ -z "${screensaver}" ]]; then
        screensaver=None
        echo "No screensaver detected"
    fi

    }

function icon_into_systray() {

    # launch icon into systray
    ${pwd}/indicator.py &

    }

function in_array() {

    # equivalent to PHP in_array
    # call: in_array needle array

    local i=0 needle="$1" IFS=" "; shift; read -a array <<< "$@"

    while [ $i -le ${#array[@]} ]; do
        if [[ "${array[$i]}" == "${needle}" ]]; then return 0; fi # true
        let i=i+1
    done
    return 1

    unset i needle IFS array

}

function isAppRunning() {
    # check if active windows is mplayer, vlc or firefox

    #Get title of active window
    activ_win_id="$(xprop -id ${activ_win_id})"

    activ_win_pid="$(grep "_NET_WM_PID(CARDINAL)" <<< "${activ_win_id}")"
    activ_win_pid=${activ_win_pid##* }

    activ_win_title="$(grep "WM_CLASS(STRING)" <<< "${activ_win_id}")"   # I used WM_NAME(STRING) before, WM_CLASS more accurate.

    activ_app_name="$(echo "${activ_win_title}" | awk -F "," '{print $2}'  | tr -s ' ')"  # just name app
    activ_app_name="${activ_app_name:2:-1}"

    app_name="$(awk '{print tolower($0)}' <<< "${activ_app_name}")"   # app name string lower

    if in_array "${app_name}" "${APPS[@]}"; then

        case "${app_name}" in

            "chromium"|"firefox"|"google-chrome"|"opera")
                # detect if flashplayer run
                if $(lsof -p ${activ_win_pid} | grep flashplayer.so); then
                    process=$(pidof "${activ_app_name}")
                else
                    # other method to detect if flashplayer run
                    case "${app_name}" in
                        "chromium")
                            if [[ "$activ_win_title" = *exe* ]]; then
                                process=$(pgrep -lfc ".*((c|C)hrome|chromium).*flashp.*")
                            fi
                        ;;
                        "firefox")
                            if [[ "$activ_win_title" = *unknown* || "$activ_win_title" = *plugin-container* ]]; then
                                process=$(pgrep -l plugin-containe | grep -wc plugin-containe)
                            fi
                        ;;
                    esac

                fi

                if [[ -z "${process}" && "${activ_win_title}" = *${activ_app_name}* ]]; then
                    process=$(pidof "${activ_app_name}")
                fi

            ;;

            *)
                if [[ "${activ_win_title}" = *${activ_app_name}* ]]; then
                    process=$(pidof "${activ_app_name}")
                fi
            ;;
        esac

    fi

    if [[ -n ${process} ]]; then return 0; else return 1; fi

    }

function delayScreensaver() {

    # reset inactivity time counter so screensaver is not started
    case "${screensaver}" in
        "cinnamon-screensaver") cinnamon-screensaver-command --deactivate > /dev/null ;;
        "gnome-screensaver") gnome-screensaver-command --deactivate > /dev/null ;;
        "kscreensaver") qdbus org.freedesktop.ScreenSaver /ScreenSaver SimulateUserActivity > /dev/null ;;
        "xautolock")
            xautolock -disable
            xautolock -enable
        ;;
        "xscreensaver") xscreensaver-command -deactivate > /dev/null ;;
    esac

    #Check if DPMS is on. If it is, deactivate and reactivate again. If it is not, do nothing.
    dpmsStatus="$(xset -q | grep -ce 'DPMS is Enabled')"
    if [ ${dpmsStatus} -eq 1 ]; then xset -dpms; fi

}

function manage_pid() {

    pid="${$}"

    if [[ -e "${LOCKFILE}" ]]; then
        if [[ ! -d /proc/$(cat "${LOCKFILE}") ]]; then
            rm "${LOCKFILE}"
            stop
        else
            pid_lf=$(<"${LOCKFILE}")
        fi

        if [[ ${pid} && ${pid_lf} ]]; then
            if [[ "${delay}" == "stop" ]]; then pid=${pid_lf}; fi
            stop
        fi
    else
        echo "${pid}" > "${LOCKFILE}"
    fi

    }

function start() {

    manage_pid
    test_delay

    icon_into_systray

    detect_id_displays
    detect_screensaver_used

    while true; do
        checkDelayProgs
        checkFullscreen
        sleep ${delay}
    done

    }

function stop() {

    kill -9 ${pid}
    if [[ -e "${LOCKFILE}" ]]; then rm "${LOCKFILE}"; fi

    exit 0

    }

function test_delay() {

    # If argument empty, use 50 seconds as default.
    if [ -z "${delay}" ]; then delay=50; fi

    if [[ ${delay} = *[^0-9]* ]]; then
        # If argument is not integer quit.
        echo "The Argument '${delay}' is not valid, not an integer"
        echo "Please use the time in seconds you want the checks to repeat."
        echo "You want it to be ~10 seconds less than the time it takes your screensaver or DPMS to activate"
        exit 1
    fi

}

start
