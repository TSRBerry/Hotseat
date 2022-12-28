##############################################################
# Hotseat App by kotor&rayk
# Version: Hotseat 0.7
##############################################################

import ac
import acsys
import traceback
import time
import os
import os.path
import configparser
# import ctypes.wintypes
from ctypes import create_unicode_buffer
from ctypes import windll
import sys
import platform
# import winsound


DEBUG = True

def debug(msg):
    if DEBUG:
        ac.log("[DEBUG] " + str(time.strftime("%H:%M:%S", time.gmtime())) + " > " + msg)
    ac.console(str(time.strftime("%H:%M:%S", time.gmtime())) + " > " + msg)

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + '/stdlib64'
else:
    sysdir = os.path.dirname(__file__) + '/stdlib'
sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

from sim_info import info
from ctypes import wintypes

#debug(os.environ['PATH'])
debug("PLATFORM RESOURCES FROM: " + sysdir)

# My Documents
CSIDL_PERSONAL = 5
# Get current, not default value
SHGFP_TYPE_CURRENT = 0

buf = create_unicode_buffer(wintypes.MAX_PATH)
windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

debug("YOUR WINDOWS DOCUMENTS FOLDER: " + buf.value)
# print(buf.value)

# path to stored car setups by driver, track and car by Assetto Corsa
#setups_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Assetto Corsa', 'setups')
setups_path = os.path.join(buf.value, 'Assetto Corsa', 'setups')

# path to all config files from Hotseat app
config_path = os.path.join(os.getcwd(), 'apps', 'python', 'Hotseat', 'ini')

# path to file with driver names
driver_names_path = os.path.join(config_path, 'drivers.ini')

# path to all driver data of this app
driver_config_path = None

appWindow = 0
app_size_x = 401
app_size_y = 293

loaded = False
driver = None
driver_config = None

bestlap = 0
drivenlaps = 0

lapcount = 0
line = None

boa_lap = 0
boa_driver = "---"

boa_section1_driver = "---"
boa_section2_driver = "---"
boa_section3_driver = "---"

boa_section1 = 0
boa_section2 = 0
boa_section3 = 0

best_section1 = 0
best_section2 = 0
best_section3 = 0

track = None
car = None

v_bestlap = 0
v_lapcount = 0
v_boalap = 0
v_driver = None
v_boadriver = None

l_lapcount = None
l_bestlap = None
l_boalap = None
l_driver = None
l_boadriver = None

l_sector1 = None
l_sector2 = None
l_sector3 = None

yl_sector1 = None
yl_sector2 = None
yl_sector3 = None

v_sector1_driver = None
v_sector2_driver = None
v_sector3_driver = None

v_sector1_time = 0
v_sector2_time = 0
v_sector3_time = 0

yv_sector1_time = 0
yv_sector2_time = 0
yv_sector3_time = 0

l_optimal = None
v_optimal = 0
optimal = 0

logo = 0
app = 0

first_run = True

# snd_sector1 = "apps/python/Hotseat/snd/1.wav"
# snd_sector2 = "apps/python/Hotseat/snd/2.wav"
# snd_sector3 = "apps/python/Hotseat/snd/3.wav"

snd_sector1faster_boa = "apps/python/Hotseat/snd/4.wav"
snd_sector2faster_boa = "apps/python/Hotseat/snd/5.wav"
snd_sector3faster_boa = "apps/python/Hotseat/snd/6.wav"

# snd_sectors_nobest = "apps/python/Hotseat/snd/7.wav"
# snd_bestlap = "apps/python/Hotseat/snd/8.wav"

# snd_sector12 = "apps/python/Hotseat/snd/9.wav"
# snd_sector23 = "apps/python/Hotseat/snd/10.wav"
# snd_sector13 = "apps/python/Hotseat/snd/11.wav"

# snd_sector12faster_boa = "apps/python/Hotseat/snd/12.wav"
# snd_sector23faster_boa = "apps/python/Hotseat/snd/13.wav"
# snd_sector13faster_boa = "apps/python/Hotseat/snd/14.wav"

# snd_combi12 = "apps/python/Hotseat/snd/15.wav"
# snd_combi23 = "apps/python/Hotseat/snd/16.wav"
# snd_combi13 = "apps/python/Hotseat/snd/17.wav"

colors = {
    "white": [255, 255, 255],
    "yellow": [247, 183, 9],
    "green": [2, 221, 20],
    "red": [252, 35, 35],
    "purple": [238, 130, 238],
    "grey": [119, 136, 153]
}


def rgb(color, a=1, bg=False):
    r = color[0] / 255
    g = color[1] / 255
    b = color[2] / 255
    if bg == False:
        return r, g, b, a
    else:
        return r, g, b


def timeToMinSecMsecTuple(t):
    mins = t // (60 * 1000)
    secs = (t - 60 * 1000 * mins) // 1000
    msecs = (t - 60 * 1000 * mins - secs * 1000)
    return (mins, secs, msecs)


def formatTime(t):
    mins, secs, msecs = timeToMinSecMsecTuple(abs(t))
    time = "%02d:%02d.%03d" % (mins, secs, msecs)
    return time


def getConfigFile(config_path):
    config = configparser.RawConfigParser()
    config.read(config_path)
    return config


def writeConfigFile(config, config_path):
    # debug("CONFIG: " + config_path + " written")
    with open(config_path, 'w') as config_file:
        config.write(config_file)
    debug("DATA SAVED TO FILE")


def getLoadedConfig(path):
    latest_atime = 0.0
    latest_file = ''
    for r, d, f in os.walk(path):
        for ini in f:
            if ini.endswith('ini') and not ini.startswith('last.ini'):
                afile = os.path.join(r, ini)
                atime = os.stat(afile).st_mtime
                if (atime - latest_atime) > 0:
                    latest_atime = atime
                    latest_file = os.path.basename(afile)
    debug("LAST CAR SETUP LOADED/SAVED: " + latest_file)
    return latest_file


def driverInit():
    global setups_path, config_path, driver_names_path, driver_config_path
    global driver_config, driver, bestlap, drivenlaps, track, car
    global best_section1, best_section2, best_section3

    try:
        track = ac.getTrackName(0)
        car = ac.getCarName(0)

        loaded_config = getLoadedConfig(setups_path)
        # debug("CONFIG LOADED: " + loaded_config)
        drivers = getConfigFile(driver_names_path)

        driver = drivers.get('driver', loaded_config)

        driver_config_path = os.path.join(config_path, loaded_config)
        # debug("driver config path: " + driver_config_path)
        driver_config = getConfigFile(driver_config_path)
        debug("CURRENT DRIVER: " + driver)

        if driver_config.has_section(track + '#' + car):
            bestlap = int(driver_config.get(track + '#' + car, 'bestlap'))
            drivenlaps = int(driver_config.get(track + '#' + car, 'drivenlaps'))
            best_section1 = int(driver_config.get(track + '#' + car, 'best_section1'))
            best_section2 = int(driver_config.get(track + '#' + car, 'best_section2'))
            best_section3 = int(driver_config.get(track + '#' + car, 'best_section3'))
        else:
            bestlap = 0
            drivenlaps = 0
            best_section1 = 0
            best_section2 = 0
            best_section3 = 0
        # debug("BEST LAP OF " + driver + ": " + formatTime(bestlap))
        # debug("DRIVEN LAPS OF " + driver + ": " + str(drivenlaps))

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        ac.console('Hotseat log - Error in driverInit (logged to file)')
        ac.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))


def trackInit():
    global driver_names_path, config_path
    global track, car, boa_lap, boa_driver
    global boa_section1, boa_section2, boa_section3, boa_section1_driver, boa_section2_driver, boa_section3_driver

    try:
        boa_driver_path = None
        boa_section1_driver_path = None
        boa_section2_driver_path = None
        boa_section3_driver_path = None
        boa_lap = 0
        boa_section1 = 0
        boa_section2 = 0
        boa_section3 = 0
        track = ac.getTrackName(0)
        car = ac.getCarName(0)
        drivers = getConfigFile(driver_names_path)
        # debug("trackInit")
        for r, d, f in os.walk(config_path):
            for ini in f:
                if ini.endswith('ini') and not ini.startswith('last.ini'):
                    afile = os.path.join(r, ini)
                    aconfig = getConfigFile(afile)
                    # debug("check configs: " +afile)

                    if aconfig.has_section(track + '#' + car):
                        if (boa_lap > int(aconfig.get(track + '#' + car, 'bestlap')) or boa_lap == 0) and int(aconfig.get(track + '#' + car, 'bestlap')) > 0:
                            debug("LOAD BEST LAPTIME EVER AND BEST DRIVER EVER")
                            boa_lap = int(aconfig.get(track + '#' + car, 'bestlap'))
                            boa_driver_path = ini
                        if (boa_section1 > int(aconfig.get(track + '#' + car, 'best_section1')) or boa_section1 == 0) and int(aconfig.get(track + '#' + car, 'best_section1')) > 0:
                            debug("LOAD BEST SECTOR1-TIME EVER AND BEST SECTOR1-DRIVER EVER")
                            boa_section1 = int(aconfig.get(track + '#' + car, 'best_section1'))
                            boa_section1_driver_path = ini
                        if (boa_section2 > int(aconfig.get(track + '#' + car, 'best_section2')) or boa_section2 == 0) and int(aconfig.get(track + '#' + car, 'best_section2')) > 0:
                            debug("LOAD BEST SECTOR2-TIME EVER AND BEST SECTOR2-DRIVER EVER")
                            boa_section2 = int(aconfig.get(track + '#' + car, 'best_section2'))
                            boa_section2_driver_path = ini
                        if (boa_section3 > int(aconfig.get(track + '#' + car, 'best_section3')) or boa_section3 == 0) and int(aconfig.get(track + '#' + car, 'best_section3')) > 0:
                            debug("LOAD BEST SECTOR3-TIME EVER AND BEST SECTOR3-DRIVER EVER")
                            boa_section3 = int(aconfig.get(track + '#' + car, 'best_section3'))
                            boa_section3_driver_path = ini

        if boa_driver_path:
            boa_driver = drivers.get("driver", boa_driver_path)
        if boa_section1_driver_path:
            boa_section1_driver = drivers.get("driver", boa_section1_driver_path)
        if boa_section2_driver_path:
            boa_section2_driver = drivers.get("driver", boa_section2_driver_path)
        if boa_section3_driver_path:
            boa_section3_driver = drivers.get("driver", boa_section3_driver_path)

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        ac.console('Hotseat log - Error in trackInit (logged to file)')
        ac.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))


def acMain(ac_version):
    global appWindow, app_size_x, app_size_y
    global driver, bestlap, boa_driver, boa_lap
    global v_driver, v_lapcount, v_bestlap
    global v_boalap, l_boalap, v_boadriver, l_boadriver
    global l_sector1, l_sector2, l_sector3
    global v_sector1_driver, v_sector2_driver, v_sector3_driver
    global v_sector1_time, v_sector2_time, v_sector3_time
    global l_optimal, v_optimal
    global boa_section1_driver, boa_section2_driver, boa_section3_driver
    global best_section1, best_section2, best_section3
    global yl_sector1, yl_sector2, yl_sector3
    global yv_sector1_time, yv_sector2_time, yv_sector3_time
    global logo, app

    try:
        ac.console("initialise app (acMain)")
        debug("'acMain' Hotseat")
        debug("ASSETTO CORSA CAR SETUPS-PATH: " + setups_path)

        trackInit()

        appWindow = ac.newApp("Hotseat")
        ac.setSize(appWindow, app_size_x, app_size_y)
        ac.drawBorder(appWindow, 1)
        logo = ac.newTexture("apps/python/Hotseat/img/logo.png")
        app = ac.newTexture("apps/python/Hotseat/img/app.png")
        ac.addRenderCallback(appWindow, onFormRender)

        # driver (first line)
        l_driver = ac.addLabel(appWindow, "Driver:")
        ac.setPosition(l_driver, 20, 40)
        ac.setFontColor(l_driver, *rgb(colors["white"]))
        
        v_driver = ac.addLabel(appWindow, "LOADING...")
        ac.setPosition(v_driver, 200, 40)
        ac.setFontColor(v_driver, *rgb(colors["red"]))
        ac.setFontAlignment(v_driver, "right")

        # laps (second line)
        l_lapcount = ac.addLabel(appWindow, "Laps:")
        ac.setPosition(l_lapcount, 20, 60)
        ac.setFontColor(l_lapcount, *rgb(colors["white"]))

        v_lapcount = ac.addLabel(appWindow, "---")
        ac.setPosition(v_lapcount, 200, 60)
        ac.setFontColor(v_lapcount, *rgb(colors["white"]))
        ac.setFontAlignment(v_lapcount, "right")

        # your best lap (third line)
        l_bestlap = ac.addLabel(appWindow, "Lap Time:")
        ac.setPosition(l_bestlap, 20, 80)
        ac.setFontColor(l_bestlap, *rgb(colors["white"]))

        v_bestlap = ac.addLabel(appWindow, "---")
        ac.setPosition(v_bestlap, 200, 80)
        ac.setFontColor(v_bestlap, *rgb(colors["white"]))
        ac.setFontAlignment(v_bestlap, "right")

        #--------------------------------------------------------------

        # your sector 1
        yl_sector1 = ac.addLabel(appWindow, "|  Sector 1:")
        ac.setPosition(yl_sector1, 220, 40)
        ac.setFontColor(yl_sector1, *rgb(colors["white"]))

        yv_sector1_time = ac.addLabel(appWindow, "---")
        ac.setPosition(yv_sector1_time, 380, 40)
        ac.setFontColor(yv_sector1_time, *rgb(colors["white"]))
        ac.setFontAlignment(yv_sector1_time, "right")

        # your sector 2
        yl_sector2 = ac.addLabel(appWindow, "|  Sector 2:")
        ac.setPosition(yl_sector2, 220, 60)
        ac.setFontColor(yl_sector2, *rgb(colors["white"]))

        yv_sector2_time = ac.addLabel(appWindow, "---")
        ac.setPosition(yv_sector2_time, 380, 60)
        ac.setFontColor(yv_sector2_time, *rgb(colors["white"]))
        ac.setFontAlignment(yv_sector2_time, "right")

        # your sector 3
        yl_sector3 = ac.addLabel(appWindow, "|  Sector 3:")
        ac.setPosition(yl_sector3, 220, 80)
        ac.setFontColor(yl_sector3, *rgb(colors["white"]))

        yv_sector3_time = ac.addLabel(appWindow, "---")
        ac.setPosition(yv_sector3_time, 380, 80)
        ac.setFontColor(yv_sector3_time, *rgb(colors["white"]))
        ac.setFontAlignment(yv_sector3_time, "right")

        # --------------------------------------------------------------

        # line1
        line = ac.addLabel(appWindow, "------------------------------------------------------------")
        ac.setPosition(line, 20, 98)
        ac.setFontColor(line, *rgb(colors["red"]))

        # best driver ever (fourth line)
        l_boadriver = ac.addLabel(appWindow, "Best Driver:")
        ac.setPosition(l_boadriver, 20, 120)
        ac.setFontColor(l_boadriver, *rgb(colors["white"]))

        v_boadriver = ac.addLabel(appWindow, boa_driver)
        ac.setPosition(v_boadriver, 200, 120)
        ac.setFontColor(v_boadriver, *rgb(colors["white"]))
        ac.setFontAlignment(v_boadriver, "right")

        # best lap ever (fifth line)
        l_boalap = ac.addLabel(appWindow, "Best Lap:")
        ac.setPosition(l_boalap, 20, 140)
        ac.setFontColor(l_boalap, *rgb(colors["white"]))

        v_boalap = ac.addLabel(appWindow, formatTime(boa_lap))
        ac.setPosition(v_boalap, 200, 140)
        ac.setFontColor(v_boalap, *rgb(colors["green"]))
        ac.setFontAlignment(v_boalap, "right")

        # BOA SECTORS !

        # Sector 1 (sixth line)
        l_sector1 = ac.addLabel(appWindow, "|  Sector 1:")
        ac.setPosition(l_sector1, 220, 120)
        ac.setFontColor(l_sector1, *rgb(colors["white"]))

        v_sector1_driver = ac.addLabel(appWindow, boa_section1_driver)
        ac.setPosition(v_sector1_driver, 317, 120)
        ac.setFontColor(v_sector1_driver, *rgb(colors["white"]))
        #ac.setFontAlignment(v_sector1_time, "left")

        v_sector1_time = ac.addLabel(appWindow, formatTime(boa_section1))
        ac.setPosition(v_sector1_time, 380, 140)
        ac.setFontColor(v_sector1_time, *rgb(colors["green"]))
        ac.setFontAlignment(v_sector1_time, "right")

        # Sector 2 (seventh line)
        l_sector2 = ac.addLabel(appWindow, "|  Sector 2:")
        ac.setPosition(l_sector2, 220, 160)
        ac.setFontColor(l_sector2, *rgb(colors["white"]))

        v_sector2_driver = ac.addLabel(appWindow, boa_section2_driver)
        ac.setPosition(v_sector2_driver, 317, 160)
        ac.setFontColor(v_sector2_driver, *rgb(colors["white"]))
        #ac.setFontAlignment(v_sector2_time, "left")

        v_sector2_time = ac.addLabel(appWindow, formatTime(boa_section2))
        ac.setPosition(v_sector2_time, 380, 180)
        ac.setFontColor(v_sector2_time, *rgb(colors["green"]))
        ac.setFontAlignment(v_sector2_time, "right")

        # Sector 3 (eigthth line)
        l_sector3 = ac.addLabel(appWindow, "|  Sector 3:")
        ac.setPosition(l_sector3, 220, 200)
        ac.setFontColor(l_sector3, *rgb(colors["white"]))

        v_sector3_driver = ac.addLabel(appWindow, boa_section3_driver)
        ac.setPosition(v_sector3_driver, 317, 200)
        ac.setFontColor(v_sector3_driver, *rgb(colors["white"]))
        #ac.setFontAlignment(v_sector3_time, "left")

        v_sector3_time = ac.addLabel(appWindow, formatTime(boa_section3))
        ac.setPosition(v_sector3_time, 380, 220)
        ac.setFontColor(v_sector3_time, *rgb(colors["green"]))
        ac.setFontAlignment(v_sector3_time, "right")

        # line3
        line = ac.addLabel(appWindow, "------------------------------------------------------------")
        ac.setPosition(line, 20, 238)
        ac.setFontColor(line, *rgb(colors["red"]))

        l_optimal = ac.addLabel(appWindow, "Optimal Best Lap:")
        ac.setPosition(l_optimal, 173, 260)
        ac.setFontColor(l_optimal, *rgb(colors["white"]))

        v_optimal = ac.addLabel(appWindow, formatTime(int(boa_section1) + int(boa_section2) + int(boa_section3)))
        #v_optimal = ac.addLabel(appWindow, formatTime(sumOptimal)
        ac.setPosition(v_optimal, 380, 260)
        ac.setFontColor(v_optimal, *rgb(colors["yellow"]))
        ac.setFontAlignment(v_optimal, "right")

        # # lines
        # line = ac.addLabel(appWindow, "|")
        # ac.setPosition(line, 72, 260)
        # ac.setFontColor(line, *rgb(colors["white"]))

        # lines
        line = ac.addLabel(appWindow, "|")
        ac.setPosition(line, 220, 140)
        ac.setFontColor(line, *rgb(colors["white"]))

        # lines
        line = ac.addLabel(appWindow, "|")
        ac.setPosition(line, 220, 180)
        ac.setFontColor(line, *rgb(colors["white"]))

        # lines
        line = ac.addLabel(appWindow, "|")
        ac.setPosition(line, 220, 220)
        ac.setFontColor(line, *rgb(colors["white"]))

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        app_error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        ac.console('Hotseat log - Error in acMAIN:')
        ac.console(app_error)
        ac.debug(app_error)

    return "Hotseat"


def onFormRender(deltaT):
    global logo, app

    try:
        ac.glQuadTextured(20, 264, 16, 16, logo)
        ac.glQuadTextured(46, 264, 16, 16, app)

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        ac.console('Hotseat log - Error in onFormRender (logged to file)')
        ac.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))


def acUpdate(deltaT):
    global v_driver, l_lapcount, v_lapcount, l_bestlap, v_bestlap
    global lapcount, bestlap, boa_driver, boa_lap, drivenlaps
    global driver_config, driver_config_path, loaded
    global v_boalap, l_boalap, v_boadriver, l_boadriver, v_optimal
    global sim_info
    global first_run, optimal
    global best_section1, best_section2, best_section3
    global boa_section1, boa_section2, boa_section3
    global boa_section1_driver, boa_section2_driver, boa_section3_driver
    global yv_sector1_time, yv_sector2_time, yv_sector3_time
    global l_sector1_driver, l_sector2_driver, l_sector3_driver
    global sectors, sector1_if2, sector2_if2, sector1_if3
    global yl_sector1, yl_sector2, yl_sector3
    global snd_bestsector1, snd_bestsector2, snd_bestsector3
    global snd_sector1, snd_sector2, snd_sector3
    global snd_sector12, snd_sector23, snd_sector13
    global snd_sector1faster_boa, snd_sector2faster_boa, snd_sector3faster_boa
    global snd_sectors_nobest, snd_bestlap
    global snd_sector12faster_boa, snd_sector23faster_boa, snd_sector13faster_boa
    global snd_combi12, snd_combi23, snd_combi13

    try:

        if ((info.graphics.iCurrentTime + info.graphics.sessionTimeLeft) < 1799000) and not loaded and not first_run:
            laps = int(ac.getCarState(0, acsys.CS.LapCount))
            best = int(ac.getCarState(0, acsys.CS.BestLap))
            splits = ac.getLastSplits(0)

            if laps > lapcount:
                lapcount = laps
                drivenlaps = drivenlaps + 1
                if not driver_config.has_section(track + '#' + car):
                    driver_config.add_section(track + '#' + car)
                driver_config.set(track + '#' + car, "drivenlaps", str(drivenlaps))
                ac.setText(v_lapcount, str(drivenlaps))
                # ADD lapcount increment
                debug("DRIVER ON TRACK AND PASSES START/FINSIH LINE")
                # debug("BEST LAP OF " + driver + ": " + formatTime(bestlap))
                # debug("THIS LAP OF " + driver + ": " + formatTime(best))
                if ((best < bestlap) or (bestlap == 0) and best > 0):
                    bestlap = best
                    # debug("new best lap: " + formatTime(bestlap))
                    ac.setText(v_bestlap, formatTime(bestlap))
                    ac.setFontColor(v_bestlap, *rgb(colors["white"]))

                    if not driver_config.has_section(track + '#' + car):
                        driver_config.add_section(track + '#' + car)
                    driver_config.set(track + '#' + car, "bestlap", str(bestlap))
                    driver_config.set(track + '#' + car, "bestlapformatted", formatTime(bestlap))
                    writeConfigFile(driver_config, driver_config_path)
                    ac.setFontColor(v_bestlap, *rgb(colors["white"]))
                    # overall best lap 
                    if (best < boa_lap) or (boa_lap == 0):
                        boa_lap = best
                        boa_driver = driver
                        ac.setText(v_boalap, formatTime(best))
                        ac.setFontColor(l_boalap, *rgb(colors["white"]))
                        ac.setFontColor(v_boalap, *rgb(colors["green"]))

                        ac.setText(v_boadriver, driver)
                        ac.setFontColor(l_boadriver, *rgb(colors["white"]))
                        ac.setFontColor(v_boadriver, *rgb(colors["white"]))
                        debug("BEST LAP TIME EVER IS FROM DRIVER: " + str(boa_driver))

                debug("GET SECTOR TIMES AFTER LAP")
                #debug("AMOUNT OF SECTORS = ", len(splits))
                for i in range(0, len(splits)):
                    debug("PROCESSING SECTORS")
                if (len(splits) == 2):
                    # boa_section3 = 0
                    # boa_section3_driver = "---"
                    yv_sector3_time = ac.addLabel(appWindow, "---")
                    ac.setFontColor(v_sector3_time, *rgb(colors["grey"]))
                    ac.setFontColor(v_sector3_driver, *rgb(colors["grey"]))
                    ac.setFontColor(yv_sector3_time, *rgb(colors["grey"]))

                # SECTOR 1
                if ((splits[0] < best_section1) or (best_section1 == 0)) and splits[0] > 0:
                    best_section1 = splits[0]
                    ac.setText(yv_sector1_time, formatTime(best_section1))
                    ac.setFontColor(yv_sector1_time, *rgb(colors["white"]))

                    if not driver_config.has_section(track + '#' + car):
                        driver_config.add_section(track + '#' + car)
                    driver_config.set(track + '#' + car, "best_section1", str(best_section1))
                    driver_config.set(track + '#' + car, "best_section1_formatted", formatTime(best_section1))
                    writeConfigFile(driver_config, driver_config_path)
                    ac.setFontColor(yv_sector1_time, *rgb(colors["white"]))
                    # overall best sector 1 
                    if (splits[0] < boa_section1) or (boa_section1 == 0):
                        boa_section1 = splits[0]
                        # winsound.PlaySound(snd_sector1faster_boa, winsound.SND_FILENAME | winsound.SND_ASYNC)
                        boa_section1_driver = driver
                        ac.setText(v_sector1_time, formatTime(splits[0]))
                        ac.setFontColor(l_sector1, *rgb(colors["white"]))
                        ac.setFontColor(v_sector1_time, *rgb(colors["green"]))
                        ac.setText(v_sector1_driver, driver)
                        ac.setFontColor(v_sector1_driver, *rgb(colors["white"]))
                        debug("BEST SECTOR1 TIME EVER IS FROM DRIVER: " + str(boa_section1_driver))

                # SECTOR 2
                if ((splits[1] < best_section2) or (best_section2 == 0)) and splits[1] > 0:
                    best_section2 = splits[1]
                    ac.setText(yv_sector2_time, formatTime(best_section2))
                    ac.setFontColor(yv_sector2_time, *rgb(colors["white"]))

                    if not driver_config.has_section(track + '#' + car):
                        driver_config.add_section(track + '#' + car)
                    driver_config.set(track + '#' + car, "best_section2", str(best_section2))
                    driver_config.set(track + '#' + car, "best_section2_formatted", formatTime(best_section2))
                    writeConfigFile(driver_config, driver_config_path)
                    ac.setFontColor(yv_sector2_time, *rgb(colors["white"]))
                    # overall best sector 2 
                    if (splits[1] < boa_section2) or (boa_section2 == 0):
                        boa_section2 = splits[1]
                        boa_section2_driver = driver
                        ac.setText(v_sector2_time, formatTime(splits[1]))
                        ac.setFontColor(l_sector2, *rgb(colors["white"]))
                        ac.setFontColor(v_sector2_time, *rgb(colors["green"]))
                        # winsound.PlaySound(snd_sector2faster_boa, winsound.SND_FILENAME | winsound.SND_ASYNC)
                        ac.setText(v_sector2_driver, driver)
                        ac.setFontColor(v_sector2_driver, *rgb(colors["white"]))
                        debug("BEST SECTOR2 TIME EVER IS FROM DRIVER: " + str(boa_section2_driver))

                # SECTOR 3
                if (len(splits) > 2) and (((splits[2] < best_section3) or (best_section3 == 0)) and splits[2] > 0):
                    best_section3 = splits[2]
                    ac.setText(yv_sector3_time, formatTime(best_section3))
                    ac.setFontColor(yv_sector3_time, *rgb(colors["white"]))

                    if not driver_config.has_section(track + '#' + car):
                        driver_config.add_section(track + '#' + car)
                    driver_config.set(track + '#' + car, "best_section3", str(best_section3))
                    driver_config.set(track + '#' + car, "best_section3_formatted", formatTime(best_section3))
                    writeConfigFile(driver_config, driver_config_path)
                    ac.setFontColor(yv_sector3_time, *rgb(colors["white"]))
                    # overall best sector 3 
                    if (splits[2] < boa_section3) or (boa_section3 == 0):
                        boa_section3 = splits[2]
                        boa_section3_driver = driver
                        ac.setText(v_sector3_time, formatTime(splits[2]))
                        ac.setFontColor(l_sector3, *rgb(colors["white"]))
                        ac.setFontColor(v_sector3_time, *rgb(colors["green"]))
                        ac.setText(v_sector3_driver, driver)
                        ac.setFontColor(v_sector3_driver, *rgb(colors["white"]))
                        debug("BEST SECTOR3 TIME EVER IS FROM DRIVER: " + str(boa_section3_driver))
                        # winsound.PlaySound(snd_sector3faster_boa, winsound.SND_FILENAME | winsound.SND_ASYNC)
                else: 
                    if not driver_config.has_section(track + '#' + car):
                        driver_config.add_section(track + '#' + car)
                    driver_config.set(track + '#' + car, "best_section3", str(0))
                    #driver_config.set(track + '#' + car, "best_section3_formatted", formatTime(best_section3))
                    writeConfigFile(driver_config, driver_config_path)

            # SOME RANDOM SOUNDS:
            #debug("CONVERT TIMES TO STR AND DETERMINE SOUND OUTPUT")
            # s0 = str(splits[0])
            # s1 = str(splits[1])
            # s2 = str(splits[2])
            # #bs1 = str(best_section1)
            # #bs2 = str(best_section2)
            # #bs3 = str(best_section3)
            boas1 = str(boa_section1)
            boas2 = str(boa_section2)
            boas3 = str(boa_section3)
            # #b = str(best)
            # #bl = str(bestlap)
            # #boal = str(boa_lap)
            optimal = (int(boas1) + int(boas2) + int(boas3))
            ac.setText(v_optimal, formatTime(optimal))
            ac.setFontColor(v_optimal, *rgb(colors["yellow"]))
            # debug("SPLITS")
            # debug(s0)
            # debug(s1)
            # debug(s2)
            # debug("BEST SECTORS")
            # debug(bs1)
            # debug(bs2)
            # debug(bs3)
            # debug("BOA SECTORS")
            # debug(boas1)
            # debug(boas2)
            # debug(boas3)
            # debug("LAP TIMES")
            # debug(b)
            # debug(bl)
            # debug(boal)

            # best sectors of all
            # if (int(s0) < int(boas1)):
                # winsound.PlaySound(snd_sector1faster_boa, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s1) < int(boas2)):
                # winsound.PlaySound(snd_sector2faster_boa, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s2) < int(boas3)):
                # winsound.PlaySound(snd_sector3faster_boa, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # # best sectors of all combinations
            # if (int(s0) < int(boas1)) and (int(s1) < int(boas2)):
                # winsound.PlaySound(snd_sector12faster_boa, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s1) < int(boas2)) and (int(s2) < int(boas3)):
                # winsound.PlaySound(snd_sector23faster_boa, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s0) < int(boas1)) and (int(s2) < int(boas3)):
                # winsound.PlaySound(snd_sector13faster_boa, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s0) < int(boas1)) and (int(s1) < int(boas2)) and (int(s2) < int(boas3)):
                # winsound.PlaySound(snd_bestlap, winsound.SND_FILENAME | winsound.SND_ASYNC)

            # your best sectors
            # if (int(s0) < int(bs1)) and (int(s0) > int(boas1)):
                # winsound.PlaySound(snd_sector1, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s1) < int(bs2)) and (int(s1) > int(boas2)):
                # winsound.PlaySound(snd_sector2, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s2) < int(bs3)) and (int(s2) > int(boas3)):
                # winsound.PlaySound(snd_sector3, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # # your best sectors combinations
            # if (int(s0) < int(bs1)) and (int(s1) < int(bs2)) and (int(s0) > int(boas1)) and (int(s1) > int(boas2)):
                # winsound.PlaySound(snd_sector12, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s1) < int(bs2)) and (int(s2) < int(bs3)) and (int(s1) > int(boas2)) and (int(s2) > int(boas3)):
                # winsound.PlaySound(snd_sector23, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s0) < int(bs1)) and (int(s2) < int(bs3)) and (int(s0) > int(boas1)) and (int(s2) > int(boas3)):
                # winsound.PlaySound(snd_sector13, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(b) < int(bl)) and (int(b) > int(boal)):
                # winsound.PlaySound(snd_sectors_nobest, winsound.SND_FILENAME | winsound.SND_ASYNC)

            # # your best sector in combination with best sectors of all
            # if (int(s0) < int(bs1)) and (int(s1) < int(boas2)):
                # winsound.PlaySound(snd_combi12, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s2) < int(bs3)) and (int(s2) < int(boas3)):
                # winsound.PlaySound(snd_combi23, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # if (int(s0) < int(bs1)) and (int(s2) < int(boas3)):
                # winsound.PlaySound(snd_combi13, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # some more are required here

        elif (((info.graphics.iCurrentTime + info.graphics.sessionTimeLeft) > 1799000) or first_run) and ac.getCarState(0, acsys.CS.Gas) and (int(ac.getCarState(0, acsys.CS.RPM)) > 0) and not loaded:
            debug("LOADING DRIVER AFTER DRIVER CHANGE OR HOTLAP START")
            driverInit()
            sum = float(info.graphics.sessionTimeLeft) + float(info.graphics.iCurrentTime)
            # debug("SESSION TIME: " + str(info.graphics.sessionTimeLeft))
            # debug("ICURRENT TIME: " + str(info.graphics.iCurrentTime))
            # debug("SUM: " + str(sum))

            # driver
            ac.setText(v_driver, driver)

            # laps
            ac.setText(v_lapcount, str(drivenlaps))
            ac.setFontColor(l_lapcount, *rgb(colors["white"]))
            ac.setFontColor(v_lapcount, *rgb(colors["white"]))

            # your best lap time
            ac.setText(v_bestlap, formatTime(bestlap))
            ac.setFontColor(l_bestlap, *rgb(colors["white"]))
            ac.setFontColor(v_bestlap, *rgb(colors["white"]))

            # your best sector1 time
            ac.setText(yv_sector1_time, formatTime(best_section1))
            ac.setFontColor(yl_sector1, *rgb(colors["white"]))
            ac.setFontColor(v_sector1_time, *rgb(colors["white"]))

            # your best sector2 time
            ac.setText(yv_sector2_time, formatTime(best_section2))
            ac.setFontColor(yl_sector2, *rgb(colors["white"]))
            ac.setFontColor(v_sector2_time, *rgb(colors["white"]))

            # your best sector3 time
            ac.setText(yv_sector3_time, formatTime(best_section3))
            ac.setFontColor(yl_sector3, *rgb(colors["white"]))
            ac.setFontColor(v_sector3_time, *rgb(colors["white"]))

            loaded = True

        elif (((info.graphics.iCurrentTime + info.graphics.sessionTimeLeft) < 1799000) or first_run) and loaded:
            # debug("Driver reset")
            debug("START DRIVING OR DRIVER RESET")
            loaded = False
            first_run = False
            lapcount = 0

        # if ac.getCarState(0, acsys.CS.LapInvalidated) == 1:
            # ac.setBackgroundTexture(appWindow, "/apps/python/Hotseat/logo_big.png")

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        ac.console('Hotseat log - Error in acUPDATE (logged to file)')
        ac.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))


def acShutdown():
    global driver_config_path, driver_config

    ac.console("shutdown app (acShutdown)")
    debug("'acShutdown' Hotseat")

    writeConfigFile(driver_config, driver_config_path)
