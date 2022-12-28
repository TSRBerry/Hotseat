# -*- coding: utf-8 -*-
import configparser
import os
from re import T
from . import utils

class Driver:
    __config_section_driverInfo = 'DriverInfo'
    __config_driverName = 'Name'
    __config_bestlap = 'bestlap'
    __config_drivenlaps = 'drivenlaps'
    __config_totaldrivenlaps = 'totaldrivenlaps'
    __config_totalTrackTime = 'TotalTrackTime'
    __config_bestSection1 = 'best_section1'
    __config_bestSection2 = 'best_section2'
    __config_bestSection3 = 'best_section3'

    def __checkConfigValue(self, config_num, new_num) -> bool:
        if config_num > 0:
            return config_num > new_num
        else:
            return new_num > 0
    
    def __getDriverFileName(self, filename) -> str:
        return filename.replace(" ", "_").lower() + ".ini"
    
    def __getDriverName(self, name) -> str:
        result = ""
        for part in name.split(" "):
            result +=  part.capitalize() + " "
        return result.rstrip() if ( len(result.rstrip()) > 0 ) else "?"
    
    def __writeConfigToDisk(self) -> None:
        if len(self.name) == 0 or self.name == "?":
            return

        with open(self.config_path, "w") as file:
            self.config.write(file)
        utils.log("[Driver] Config written to disk for: " + self.name)

    def __init__(self, filename, car_name, track_name) -> None:
        self.config_path = os.path.join(utils.config_path, "driver", self.__getDriverFileName(filename))
        self.config = utils.getOrCreateConfigFile(self.config_path)
        self.car = car_name
        self.track = track_name
        self.section_name = self.track + '#' + self.car

        if not self.config.has_section(self.__config_section_driverInfo):
            self.config.add_section(self.__config_section_driverInfo)
            self.config.set(self.__config_section_driverInfo, self.__config_driverName, self.__getDriverName(filename))
            with open(self.config_path, "w") as file:
                self.config.write(file)
            self.name = self.__getDriverName(filename)
        else:
            self.name = self.config.get(self.__config_section_driverInfo, self.__config_driverName)

        if self.config.has_section(self.section_name):
            try:
                self.bestlap = int(self.config.get(self.section_name, self.__config_bestlap))
            except configparser.NoOptionError:
                self.bestlap = 0
            try:
                self.drivenlaps = int(self.config.get(self.section_name, self.__config_drivenlaps))
            except configparser.NoOptionError:
                self.drivenlaps = 0
            try:
                self.totaldrivenlaps = int(self.config.get(self.section_name, self.__config_totaldrivenlaps))
                if self.totaldrivenlaps < self.drivenlaps:
                    self.totaldrivenlaps += self.drivenlaps - self.totaldrivenlaps
            except configparser.NoOptionError:
                self.totaldrivenlaps = self.drivenlaps
            try:
                self.totaltracktime = int(self.config.get(self.section_name, self.__config_totalTrackTime))
                if self.totaltracktime < self.bestlap:
                    self.totaltracktime += self.bestlap - self.totaltracktime
            except configparser.NoOptionError:
                self.totaltracktime = self.bestlap
            try:
                self.best_sections = [
                    int(self.config.get(self.section_name, self.__config_bestSection1)),
                    int(self.config.get(self.section_name, self.__config_bestSection2)),
                    int(self.config.get(self.section_name, self.__config_bestSection3))
                ]
            except (ValueError, configparser.NoOptionError):
                self.best_sections = [0, 0, 0]
        else:
            self.config.add_section(self.section_name)
            self.totaltracktime = 0
            self.bestlap = 0
            self.drivenlaps = 0
            self.totaldrivenlaps = 0
            self.best_sections = [0, 0, 0]
        
        utils.log("[Driver] Data: " + str([self.config_path, self.car, self.track, self.section_name, self.name, self.bestlap, self.drivenlaps, self.best_sections]))
        utils.log("[Driver] Init done for driver: " + self.name)
        self.__writeConfig()
    
    def getBestLapFormatted(self) -> str:
        return utils.formatTime(self.bestlap)
    
    def getBestSectionFormatted(self, index) -> str:
        if index < 3:
            return utils.formatTime(self.best_sections[index])
        else:
            raise IndexError

    def __writeLap(self, timeInMs, invalid=False) -> bool:
        result = False
        if timeInMs > 0:
            if not invalid:
                if self.bestlap == 0:
                    utils.log("[Driver] Writing first best lap for driver: " + self.name)
                    self.bestlap = timeInMs
                    result = True
                else:
                    if self.bestlap > timeInMs:
                        utils.log("[Driver] Writing new best lap for driver: " + self.name)
                        self.bestlap = timeInMs
                        result = True
                self.drivenlaps += 1
            else:
                self.totaldrivenlaps += 1
            self.totaltracktime += timeInMs
        return result

    def __writeSections(self, sections) -> bool:
        result = False
        for i in range(3):
            if len(sections) >= (i + 1):
                if sections[i] > 0:
                    if self.best_sections[i] == 0:
                        utils.log("[Driver] Writing first best section " + str(i) + " for driver: " + self.name)
                        self.best_sections[i] = sections[i]
                        result = True
                    else:
                        if self.best_sections[i] > sections[i]:
                            utils.log("[Driver] Writing new best section " + str(i) + " for driver: " + self.name)
                            self.best_sections[i] = sections[i]
                            result = True
        return result

    def __writeConfig(self) -> None:
        # Do some sanity checks before writing anything
        try:
            config_totaltracktime = int(self.config.get(self.section_name, self.__config_totalTrackTime))
        except (ValueError, configparser.NoOptionError):
            config_totaltracktime = 0
        if self.__checkConfigValue(config_totaltracktime, self.totaltracktime):
            self.config.set(self.section_name, self.__config_totalTrackTime, self.totaltracktime)
            self.config.set(self.section_name, self.__config_totalTrackTime + "formatted", utils.formatTime(self.totaltracktime))
       
        try:
            config_bestlap = int(self.config.get(self.section_name, self.__config_bestlap))
        except (ValueError, configparser.NoOptionError):
            config_bestlap = 0
        if self.__checkConfigValue(config_bestlap, self.bestlap):
            self.config.set(self.section_name, self.__config_bestlap, self.bestlap)
            self.config.set(self.section_name, self.__config_bestlap + "formatted", self.getBestLapFormatted())
       
        try:
            config_drivenlaps = int(self.config.get(self.section_name, self.__config_drivenlaps))
        except configparser.NoOptionError:
            config_drivenlaps = 0
        if self.__checkConfigValue(config_drivenlaps, self.drivenlaps):
            self.config.set(self.section_name, self.__config_drivenlaps, self.drivenlaps)

        try:
            config_totaldrivenlaps = int(self.config.get(self.section_name, self.__config_totaldrivenlaps))
        except configparser.NoOptionError:
            config_totaldrivenlaps = 0
        if self.__checkConfigValue(config_totaldrivenlaps, self.totaldrivenlaps):
            self.config.set(self.section_name, self.__config_totaldrivenlaps, self.totaldrivenlaps)
       
        try:
            config_bestSection1 = int(self.config.get(self.section_name, self.__config_bestSection1))
        except (ValueError, configparser.NoOptionError):
            config_bestSection1 = 0
        if self.__checkConfigValue(config_bestSection1, self.best_sections[0]):
            self.config.set(self.section_name, self.__config_bestSection1, self.best_sections[0])
            self.config.set(self.section_name, self.__config_bestSection1 + "formatted", self.getBestSectionFormatted(0))
       
        try:
            config_bestSection2 = int(self.config.get(self.section_name, self.__config_bestSection2))
        except (ValueError, configparser.NoOptionError):
            config_bestSection2 = 0
        if self.__checkConfigValue(config_bestSection2, self.best_sections[1]):
            self.config.set(self.section_name, self.__config_bestSection2, self.best_sections[1])
            self.config.set(self.section_name, self.__config_bestSection2 + "formatted", self.getBestSectionFormatted(1))
       
        try:
            config_bestSection3 = int(self.config.get(self.section_name, self.__config_bestSection3))
        except (ValueError, configparser.NoOptionError):
            config_bestSection3 = 0
        if self.__checkConfigValue(config_bestSection3, self.best_sections[2]):
            self.config.set(self.section_name, self.__config_bestSection3, self.best_sections[2])
            self.config.set(self.section_name, self.__config_bestSection3 + "formatted", self.getBestSectionFormatted(2))

        self.__writeConfigToDisk()
        utils.log("[Driver] Config updated for driver " + self.name)
    
    def cmpAndWriteResults(self, lap_timeInMs, sections, invalid=False) -> bool:
        result = self.__writeLap(lap_timeInMs, invalid)
        if self.__writeSections(sections):
            result = True
        self.__writeConfig()
        return result
