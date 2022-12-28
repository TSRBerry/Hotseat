# -*- coding: utf-8 -*-
##############################################################
# Hotseat App by kotor&rayk
# Rewritten by TSR Berry <20988865+TSRBerry@users.noreply.github.com>
# Version: Hotseat 0.7.1
##############################################################

import ac
import acsys
import traceback
import os
import sys
import platform

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + '/stdlib64'
else:
    sysdir = os.path.dirname(__file__) + '/stdlib'
sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

from sim_info import info
import hs_lib.utils as utils
from hs_lib.game import Session
from hs_lib.driver import Driver

appWindow = 0
# app_size_x = 410
# app_size_y = 295
app_size_x = 401
app_size_y = 293

loaded = False
lapcount = 0
lapInvalid = False

driver = None
session = None

track = None
car = None

v_bestlap = None
v_lapcount = None
v_boalap = None
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

v_sector1_time = None
v_sector2_time = None
v_sector3_time = None

yv_sector1_time = None
yv_sector2_time = None
yv_sector3_time = None

l_optimal = None
v_optimal = None
optimal = None

enable_notifications = True

logo = 0
app = 0

first_run = True

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


def trackInit():
    global session, driver, loaded

    try:
        utils.log("<trackInit> Starting...")
        session = Session(ac.getFocusedCar())
        if session.lastDriver is not None:
            utils.log("<trackInit> Found lastDriver!")
            driver = Driver(session.lastDriver, session.car, session.track)
            loaded = True
        utils.log("<trackInit> Done...")
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        ac.console('Hotseat log - Error in trackInit (logged to file)')
        ac.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

def buildAppWindowDriver():
    global session, driver, appWindow
    global l_driver, v_driver
    global l_lapcount, v_lapcount
    global l_bestlap, v_bestlap
    global yl_sector1, yl_sector2, yl_sector3
    global yv_sector1_time, yv_sector2_time, yv_sector3_time

    # driver (first line)
    if l_driver is None:
        l_driver = ac.addLabel(appWindow, "Driver:")
        ac.setPosition(l_driver, 20, 40)
        ac.setFontColor(l_driver, *rgb(colors["white"]))
    
    val_driver = "LOADING..." if session.lastDriver is None or driver is None else driver.name
    utils.log("<acMain> First driver value: " + val_driver)
    if v_driver is None:
        v_driver = ac.addLabel(appWindow, val_driver)
        ac.setPosition(v_driver, 200, 40)
        ac.setFontColor(v_driver, *rgb(colors["red"]))
        ac.setFontAlignment(v_driver, "right")
    else:
        ac.setText(v_driver, val_driver)
    utils.log("<acMain> Driver value size: " + str(ac.getSize(v_driver)) + " pos: " + str(ac.getPosition(v_driver)))

    # laps (second line)
    if l_lapcount is None:
        l_lapcount = ac.addLabel(appWindow, "Laps:")
        ac.setPosition(l_lapcount, 20, 60)
        ac.setFontColor(l_lapcount, *rgb(colors["white"]))

    val_lapcount = "---" if session.lastDriver is None or driver is None else str(driver.drivenlaps) + " / " + str(driver.totaldrivenlaps)
    utils.log("<acMain> First laps value: " + val_lapcount)
    if v_lapcount is None:
        v_lapcount = ac.addLabel(appWindow, val_lapcount)
        ac.setPosition(v_lapcount, 200, 60)
        ac.setFontColor(v_lapcount, *rgb(colors["white"]))
        ac.setFontAlignment(v_lapcount, "right")
    else:
        ac.setText(v_lapcount, val_lapcount)
    utils.log("<acMain> Lapcount value size: " + str(ac.getSize(v_lapcount)) + " pos: " + str(ac.getPosition(v_lapcount)))

    # your best lap (third line)
    if l_bestlap is None:
        l_bestlap = ac.addLabel(appWindow, "Lap Time:")
        ac.setPosition(l_bestlap, 20, 80)
        ac.setFontColor(l_bestlap, *rgb(colors["white"]))

    val_bestlap = "---" if session.lastDriver is None or driver is None else driver.getBestLapFormatted()
    utils.log("<acMain> First bestlap value: " + val_bestlap)
    if v_bestlap is None:
        v_bestlap = ac.addLabel(appWindow, val_bestlap)
        ac.setPosition(v_bestlap, 200, 80)
        ac.setFontColor(v_bestlap, *rgb(colors["white"]))
        ac.setFontAlignment(v_bestlap, "right")
    else:
        ac.setText(v_bestlap, val_bestlap)
    utils.log("<acMain> LapTime value size: " + str(ac.getSize(v_bestlap)) + " pos: " + str(ac.getPosition(v_bestlap)))

    # -------------------------------------------------------------------

    # your sector 1
    if yl_sector1 is None:
        yl_sector1 = ac.addLabel(appWindow, "|  Sector 1:")
        ac.setPosition(yl_sector1, 220, 40)
        ac.setFontColor(yl_sector1, *rgb(colors["white"]))

    yval_sector1_time = "---" if session.lastDriver is None or driver is None else driver.getBestSectionFormatted(0)
    if yv_sector1_time is None:
        yv_sector1_time = ac.addLabel(appWindow, yval_sector1_time)
        ac.setPosition(yv_sector1_time, 380, 40)
        ac.setFontColor(yv_sector1_time, *rgb(colors["white"]))
        ac.setFontAlignment(yv_sector1_time, "right")
    else:
        ac.setText(yv_sector1_time, yval_sector1_time)

    # your sector 2
    if yl_sector2 is None:
        yl_sector2 = ac.addLabel(appWindow, "|  Sector 2:")
        ac.setPosition(yl_sector2, 220, 60)
        ac.setFontColor(yl_sector2, *rgb(colors["white"]))

    yval_sector2_time = "---" if session.lastDriver is None or driver is None else driver.getBestSectionFormatted(1)
    if yv_sector2_time is None:
        yv_sector2_time = ac.addLabel(appWindow, yval_sector2_time)
        ac.setPosition(yv_sector2_time, 380, 60)
        ac.setFontColor(yv_sector2_time, *rgb(colors["white"]))
        ac.setFontAlignment(yv_sector2_time, "right")
    else:
        ac.setText(yv_sector2_time, yval_sector2_time)

    # your sector 3
    if yl_sector3 is None:
        yl_sector3 = ac.addLabel(appWindow, "|  Sector 3:")
        ac.setPosition(yl_sector3, 220, 80)
        ac.setFontColor(yl_sector3, *rgb(colors["white"]))

    yval_sector3_time = "---" if session.lastDriver is None or driver is None else driver.getBestSectionFormatted(2)
    if yv_sector3_time is None:
        yv_sector3_time = ac.addLabel(appWindow, yval_sector3_time)
        ac.setPosition(yv_sector3_time, 380, 80)
        ac.setFontColor(yv_sector3_time, *rgb(colors["white"]))
        ac.setFontAlignment(yv_sector3_time, "right")
    else:
        ac.setText(yv_sector3_time, yval_sector3_time)

def buildAppWindowBoA():
    global session, driver
    global l_boadriver, v_boadriver
    global l_boalap, v_boalap
    global l_sector1, l_sector2, l_sector3
    global v_sector1_driver, v_sector1_time
    global v_sector2_driver, v_sector2_time
    global v_sector3_driver, v_sector3_time
    global l_optimal, v_optimal

    utils.log("<acMain> Getting first boa_lap value...")
    boa_lap = session.getBestLapFormatted()
    utils.log("<acMain> First boa_lap value: " + str(boa_lap))

    # best driver ever (fourth line)
    if l_boalap is None:
        l_boadriver = ac.addLabel(appWindow, "Best Driver:")
        ac.setPosition(l_boadriver, 20, 200)
        ac.setFontColor(l_boadriver, *rgb(colors["white"]))

    if v_boadriver is None:
        v_boadriver = ac.addLabel(appWindow, boa_lap[0])
        ac.setPosition(v_boadriver, 200, 200)
        ac.setFontColor(v_boadriver, *rgb(colors["white"]))
        ac.setFontAlignment(v_boadriver, "right")
    else:
        ac.setText(v_boadriver, boa_lap[0])

    # best lap ever (fifth line)
    if l_boalap is None:
        l_boalap = ac.addLabel(appWindow, "Best Lap:")
        ac.setPosition(l_boalap, 20, 220)
        ac.setFontColor(l_boalap, *rgb(colors["white"]))

    if v_boalap is None:
        v_boalap = ac.addLabel(appWindow, boa_lap[1])
        ac.setPosition(v_boalap, 200, 220)
        ac.setFontColor(v_boalap, *rgb(colors["green"]))
        ac.setFontAlignment(v_boalap, "right")
    else:
        ac.setText(v_boalap, boa_lap[1])

    # BOA SECTORS !

    # Sector 1 (sixth line)
    l_sector1 = ac.addLabel(appWindow, "|  Sector 1:")
    ac.setPosition(l_sector1, 220, 120)
    ac.setFontColor(l_sector1, *rgb(colors["white"]))

    boa_section1 = session.getBestSectionFormatted(0)

    if v_sector1_driver is None:
        v_sector1_driver = ac.addLabel(appWindow, boa_section1[0])
        ac.setPosition(v_sector1_driver, 317, 120)
        ac.setFontColor(v_sector1_driver, *rgb(colors["white"]))
        #ac.setFontAlignment(v_sector1_time, "left")
    else:
        ac.setText(v_sector1_driver, boa_section1[0])

    if v_sector1_time is None:
        v_sector1_time = ac.addLabel(appWindow, boa_section1[1])
        ac.setPosition(v_sector1_time, 380, 140)
        ac.setFontColor(v_sector1_time, *rgb(colors["green"]))
        ac.setFontAlignment(v_sector1_time, "right")
    else:
        ac.setText(v_sector1_time, boa_section1[1])

    # Sector 2 (seventh line)
    if l_sector2 is None:
        l_sector2 = ac.addLabel(appWindow, "|  Sector 2:")
        ac.setPosition(l_sector2, 220, 160)
        ac.setFontColor(l_sector2, *rgb(colors["white"]))

    boa_section2 = session.getBestSectionFormatted(1)

    if v_sector2_driver is None:
        v_sector2_driver = ac.addLabel(appWindow, boa_section2[0])
        ac.setPosition(v_sector2_driver, 317, 160)
        ac.setFontColor(v_sector2_driver, *rgb(colors["white"]))
        #ac.setFontAlignment(v_sector2_time, "left")
    else:
        ac.setText(v_sector2_driver, boa_section2[0])

    if v_sector2_time is None:
        v_sector2_time = ac.addLabel(appWindow, boa_section2[1])
        ac.setPosition(v_sector2_time, 380, 180)
        ac.setFontColor(v_sector2_time, *rgb(colors["green"]))
        ac.setFontAlignment(v_sector2_time, "right")
    else:
        ac.setText(v_sector2_time, boa_section2[1])

    # Sector 3 (eigthth line)
    if l_sector3 is None:
        l_sector3 = ac.addLabel(appWindow, "|  Sector 3:")
        ac.setPosition(l_sector3, 220, 200)
        ac.setFontColor(l_sector3, *rgb(colors["white"]))

    boa_section3 = session.getBestSectionFormatted(2)

    if v_sector3_driver is None:
        v_sector3_driver = ac.addLabel(appWindow, boa_section3[0])
        ac.setPosition(v_sector3_driver, 317, 200)
        ac.setFontColor(v_sector3_driver, *rgb(colors["white"]))
        #ac.setFontAlignment(v_sector3_time, "left")
    else:
        ac.setText(v_sector3_driver, boa_section3[0])

    if v_sector3_time is None:
        v_sector3_time = ac.addLabel(appWindow, boa_section3[1])
        ac.setPosition(v_sector3_time, 380, 220)
        ac.setFontColor(v_sector3_time, *rgb(colors["green"]))
        ac.setFontAlignment(v_sector3_time, "right")
    else:
        ac.setText(v_sector3_time, boa_section3[1])


    if l_optimal is None:
        l_optimal = ac.addLabel(appWindow, "Optimal Best Lap:")
        ac.setPosition(l_optimal, 173, 260)
        ac.setFontColor(l_optimal, *rgb(colors["white"]))

    if v_optimal is None:
        v_optimal = ac.addLabel(appWindow, session.getOptimalLapTimeFormatted())
        ac.setPosition(v_optimal, 380, 260)
        ac.setFontColor(v_optimal, *rgb(colors["yellow"]))
        ac.setFontAlignment(v_optimal, "right")
    else:
        ac.setText(v_optimal, session.getOptimalLapTimeFormatted())


def changeDriverBtnCallback(dummy, variable):
    global driver, session
    global b_changeDriver, it_driverName, l_driverName
    global enable_notifications
    
    enable_notifications = False
    ac.setVisible(b_changeDriver, 0)
    ac.setVisible(l_driverName, 1)
    ac.setVisible(it_driverName, 1)
    ac.setFocus(it_driverName, 1)

    driver = None

def driverNameInputCallback(string):
    global driver, session
    global b_changeDriver, it_driverName, l_driverName
    global enable_notifications

    text = ac.getText(it_driverName)
    if len(text.strip()) > 0 and text.strip() != "?":
        driver = Driver(text, session.car, session.track)
        session.setLastDriver(driver.name)
        buildAppWindowDriver()

    ac.setFocus(it_driverName, 0)
    ac.setVisible(it_driverName, 0)
    ac.setVisible(l_driverName, 0)
    ac.setText(it_driverName, "")
    ac.setVisible(b_changeDriver, 1)
    enable_notifications = True


def acMain(ac_version):
    global driver, session
    global b_changeDriver, it_driverName, l_driverName
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
    global logo, app, enable_notifications

    try:
        ac.console("Initialise App (acMain)")
        utils.log("'acMain' Hotseat")

        trackInit()

        appWindow = ac.newApp("Hotseat")
        ac.setSize(appWindow, app_size_x, app_size_y)
        ac.drawBorder(appWindow, 1)
        logo = ac.newTexture("apps/python/Hotseat/img/logo.png")
        app = ac.newTexture("apps/python/Hotseat/img/app.png")
        ac.addRenderCallback(appWindow, onFormRender)

        utils.log("<acMain> Building appWindow...")

        #--------------------------------------------------------------
        
        buildAppWindowDriver()

        # --------------------------------------------------------------

        # line1
        line = ac.addLabel(appWindow, "------------------------------------------------------------")
        ac.setPosition(line, 20, 98)
        ac.setFontColor(line, *rgb(colors["red"]))

        # change driver button
        # old line height: 120
        b_changeDriver = ac.addButton(appWindow, "Change Driver")
        ac.setSize(b_changeDriver, 180, 25)
        ac.setPosition(b_changeDriver, 20, 160)
        ac.addOnClickedListener(b_changeDriver, changeDriverBtnCallback)

        # change driver name label
        l_driverName = ac.addLabel(appWindow, "Enter Name:")
        ac.setPosition(l_driverName, 20, 120)
        ac.setFontColor(l_driverName, *rgb(colors["white"]))
        ac.setVisible(l_driverName, 0)

        # change driver input box
        it_driverName = ac.addTextInput(appWindow, "Name")
        ac.setSize(it_driverName, 180, 25)
        ac.setPosition(it_driverName, 20, 140)
        ac.setVisible(it_driverName, 0)
        ac.addOnValidateListener(it_driverName, driverNameInputCallback)
        enable_notifications = True

        # --------------------------------------------

        buildAppWindowBoA()

        # line3
        line = ac.addLabel(appWindow, "------------------------------------------------------------")
        ac.setPosition(line, 20, 238)
        ac.setFontColor(line, *rgb(colors["red"]))

        # --------------------------------------------

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

        utils.log("<acMain> appWindow done.")

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        app_error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        ac.console('Hotseat log - Error in acMAIN:')
        ac.console(app_error)

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
    global b_changeDriver, it_driverName, l_driverName
    global loaded, lapcount, lapInvalid
    global session, driver
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
            laps = int(ac.getCarState(session.car_id, acsys.CS.LapCount))
            last = int(ac.getCarState(session.car_id, acsys.CS.LastLap))
            splits = ac.getLastSplits(session.car_id)

            if laps > lapcount:
                lapcount = laps
                utils.log("DRIVER ON TRACK AND PASSES START/FINSIH LINE")
                if driver.cmpAndWriteResults(last, splits, lapInvalid):
                    if not lapInvalid:
                        utils.log("Lap is valid")
                        
                        ac.setText(v_bestlap, driver.getBestLapFormatted())
                        ac.setFontColor(v_bestlap, *rgb(colors["white"]))

                        # SECTOR 1
                        ac.setText(yv_sector1_time, driver.getBestSectionFormatted(0))
                        ac.setFontColor(yv_sector1_time, *rgb(colors["white"]))

                        # SECTOR 2
                        ac.setText(yv_sector2_time, driver.getBestSectionFormatted(1))
                        ac.setFontColor(yv_sector2_time, *rgb(colors["white"]))

                        # SECTOR 3
                        ac.setText(yv_sector3_time, driver.getBestSectionFormatted(2))
                        ac.setFontColor(yv_sector3_time, *rgb(colors["white"]))


                        if session.cmpAndWriteResults(driver.name, last, splits):
                            ac.setText(v_boalap, session.getBestLapFormatted()[1])
                            ac.setFontColor(l_boalap, *rgb(colors["white"]))
                            ac.setFontColor(v_boalap, *rgb(colors["green"]))

                            ac.setText(v_boadriver, session.getBestLapFormatted()[0])
                            ac.setFontColor(l_boadriver, *rgb(colors["white"]))
                            ac.setFontColor(v_boadriver, *rgb(colors["white"]))
                            utils.log("BEST LAP TIME EVER IS FROM DRIVER: " +
                                      str(session.getBestLapFormatted()[0]))
                            
                            # overall best sector 1 
                            ac.setText(v_sector1_time, session.getBestSectionFormatted(0)[1])
                            ac.setFontColor(l_sector1, *rgb(colors["white"]))
                            ac.setFontColor(v_sector1_time, *rgb(colors["green"]))
                            ac.setText(v_sector1_driver, session.getBestSectionFormatted(0)[0])
                            ac.setFontColor(v_sector1_driver, *rgb(colors["white"]))
                            utils.log("BEST SECTOR1 TIME EVER IS FROM DRIVER: " +
                                  str(session.getBestSectionFormatted(0)[0]))

                            # overall best sector 2 
                            ac.setText(v_sector2_time, session.getBestSectionFormatted(1)[1])
                            ac.setFontColor(l_sector2, *rgb(colors["white"]))
                            ac.setFontColor(v_sector2_time, *rgb(colors["green"]))
                            ac.setText(v_sector2_driver, session.getBestSectionFormatted(1)[0])
                            ac.setFontColor(v_sector2_driver, *rgb(colors["white"]))
                            utils.log("BEST SECTOR2 TIME EVER IS FROM DRIVER: " +
                                      str(session.getBestSectionFormatted(1)[0]))

                            # overall best sector 3 
                            ac.setText(v_sector3_time, session.getBestSectionFormatted(2)[1])
                            ac.setFontColor(l_sector3, *rgb(colors["white"]))
                            ac.setFontColor(v_sector3_time, *rgb(colors["green"]))
                            ac.setText(v_sector3_driver, session.getBestSectionFormatted(2)[0])
                            ac.setFontColor(v_sector3_driver, *rgb(colors["white"]))
                            utils.log("BEST SECTOR3 TIME EVER IS FROM DRIVER: " +
                                  str(session.getBestSectionFormatted(2)[0]))
                
                ac.setText(v_lapcount, str(driver.drivenlaps) + " / " + str(driver.totaldrivenlaps))

                if (len(splits) == 2):
                    yv_sector3_time = ac.addLabel(appWindow, "---")
                    ac.setFontColor(v_sector3_time, *rgb(colors["grey"]))
                    ac.setFontColor(v_sector3_driver, *rgb(colors["grey"]))
                    ac.setFontColor(yv_sector3_time, *rgb(colors["grey"]))
                
                lapInvalid = False
                utils.log("<acUpdate> LapInvalid changed: " + str(lapInvalid))

            else:
                #Lap validity check (copied from Sidekick)
                tiresOutValue = info.physics.numberOfTyresOut
                carWasInPit = ac.isCarInPitline(session.car_id)
                carWasDrivenByAI = info.physics.isAIControlled
                if not lapInvalid and (tiresOutValue > 2 or carWasInPit or carWasDrivenByAI):
                    lapInvalid = True
                    utils.log("<acUpdate> LapInvalid changed: " + str(lapInvalid))

            ac.setText(v_optimal, session.getOptimalLapTimeFormatted())
            ac.setFontColor(v_optimal, *rgb(colors["yellow"]))

        elif (((info.graphics.iCurrentTime + info.graphics.sessionTimeLeft) > 1799000) or first_run) and ac.getCarState(0, acsys.CS.Gas) and (int(ac.getCarState(0, acsys.CS.RPM)) > 0) and not loaded:
            utils.log("LOADING DRIVER AFTER DRIVER CHANGE OR HOTLAP START")

            if driver is not None:
                # driver
                ac.setText(v_driver, driver)

                # laps
                ac.setText(v_lapcount, str(driver.drivenlaps))
                ac.setFontColor(l_lapcount, *rgb(colors["white"]))
                ac.setFontColor(v_lapcount, *rgb(colors["white"]))

                # your best lap time
                ac.setText(v_bestlap, driver.getBestLapFormatted())
                ac.setFontColor(l_bestlap, *rgb(colors["white"]))
                ac.setFontColor(v_bestlap, *rgb(colors["white"]))

                # your best sector1 time
                ac.setText(yv_sector1_time, driver.getBestSectionFormatted(0))
                ac.setFontColor(yl_sector1, *rgb(colors["white"]))
                ac.setFontColor(v_sector1_time, *rgb(colors["white"]))

                # your best sector2 time
                ac.setText(yv_sector2_time, driver.getBestSectionFormatted(1))
                ac.setFontColor(yl_sector2, *rgb(colors["white"]))
                ac.setFontColor(v_sector2_time, *rgb(colors["white"]))

                # your best sector3 time
                ac.setText(yv_sector3_time, driver.getBestSectionFormatted(2))
                ac.setFontColor(yl_sector3, *rgb(colors["white"]))
                ac.setFontColor(v_sector3_time, *rgb(colors["white"]))

                loaded = True

        elif (((info.graphics.iCurrentTime + info.graphics.sessionTimeLeft) < 1799000) or first_run) and loaded:
            utils.log("START DRIVING OR DRIVER RESET")
            loaded = False
            first_run = False
            lapcount = 0

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        ac.console('Hotseat log - Error in acUPDATE (logged to file)')
        ac.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))


def acShutdown():
    ac.console("shutdown app (acShutdown)")
    utils.log("'acShutdown' Hotseat")
