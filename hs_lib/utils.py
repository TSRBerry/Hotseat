# -*- coding: utf-8 -*-
import configparser
import time
import os
import ac

config_path = os.path.join(os.getcwd(), 'apps', 'python', 'Hotseat', 'ini')

def log(msg) -> None:
    ac.log("[" + str(time.strftime("%H:%M:%S", time.gmtime())) + "] " + msg)
    ac.console("[" + str(time.strftime("%H:%M:%S", time.gmtime())) + "] " + msg)

def getConfigFile(config_path) -> configparser.RawConfigParser:
    config = configparser.RawConfigParser()
    config.read(config_path)
    return config

def getOrCreateConfigFile(config_path) -> configparser.RawConfigParser:
    if os.path.isfile(config_path):
        return getConfigFile(config_path)
    else:
        config = configparser.RawConfigParser()
        with open(config_path, "w") as file:
            config.write(file)
        return config


def timeToMinSecMsecTuple(t) -> tuple:
    mins = t // (60 * 1000)
    secs = (t - 60 * 1000 * mins) // 1000
    msecs = (t - 60 * 1000 * mins - secs * 1000)
    return (mins, secs, msecs)


def formatTime(t) -> str:
    mins, secs, msecs = timeToMinSecMsecTuple(abs(t))
    time = "%02d:%02d.%03d" % (mins, secs, msecs)
    return time

def formattedTimetoMs(fmt_time) -> int:
    fmt_time = fmt_time.split(":")
    return (int(fmt_time[0]) * 60 + int(fmt_time[1])) * 1000 + int(fmt_time[2])
