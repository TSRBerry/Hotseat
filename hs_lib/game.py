# -*- coding: utf-8 -*-
import ac
import os
from . import utils
from .driver import Driver

# Session = Track + Car
class Session:
    def __init__(self, car_id) -> None:
        utils.log("[Session] Init start")
        self.car_id = car_id
        self.car = ac.getCarName(self.car_id)
        self.track = ac.getTrackName(self.car_id)
        self.bestlap = self.__getBestLap()
        self.best_sections = self.__getBestSections()

        self.lastDriver_cfg = None
        self.lastDriver = self.__getLastDriver()
        utils.log("[Session] Data: " + str([self.car_id, self.car, self.track, self.bestlap, self.best_sections, self.lastDriver]))
        utils.log("[Session] Init done")

    def __getLastDriver(self) -> str:
        self.lastDriver_cfg = utils.getOrCreateConfigFile(os.path.join(utils.config_path, "last.ini"))
        if self.lastDriver_cfg.has_section("LastDriver"):
            return self.lastDriver_cfg.get("LastDriver", "name")
        else:
            self.lastDriver_cfg.add_section("LastDriver")
            self.lastDriver_cfg.set("LastDriver", "name", "")
            with open(os.path.join(utils.config_path, "last.ini"), "w") as file:
                self.lastDriver_cfg.write(file)
            return None

    def setLastDriver(self, driver_name) -> None:
        if driver_name != self.lastDriver:
            self.lastDriver = driver_name
            self.lastDriver_cfg.set("LastDriver", "name", self.lastDriver)
            with open(os.path.join(utils.config_path, "last.ini"), "w") as file:
                self.lastDriver_cfg.write(file)

    def __getBestLap(self) -> tuple:
        bestlap = 0
        bestdriver = None
        for file in os.listdir(os.path.join(utils.config_path, "driver")):
            if file == "last.ini" or not file.endswith(".ini"):
                continue

            temp_driver = Driver(file.replace(".ini", ""), self.car, self.track)
            if temp_driver.bestlap == 0:
                continue
            if bestlap == 0:
                bestlap = temp_driver.bestlap
                bestdriver = temp_driver.name
            else:
                if temp_driver.bestlap < bestlap:
                    bestlap = temp_driver.bestlap
                    bestdriver = temp_driver.name
        return (bestdriver, bestlap)

    def __getBestSections(self) -> list:
        bestsections = [(None, 0), (None, 0), (None, 0)]
        for file in os.listdir(os.path.join(utils.config_path, "driver")):
            if file == "last.ini" or not file.endswith(".ini"):
                continue

            temp_driver = Driver(file.replace(".ini", ""), self.car, self.track)
            for i in range(3):
                if temp_driver.best_sections[i] == 0:
                    continue
                if bestsections[i][1] == 0:
                    bestsections[i] = temp_driver.name, temp_driver.best_sections[i]
                else:
                    if temp_driver.best_sections[i] < bestsections[i][1]:
                        bestsections[i] = temp_driver.name, temp_driver.best_sections[i]
        return bestsections

    def __writeLap(self, driver_name, timeInMs) -> bool:
        if timeInMs > 0:
            if self.bestlap[1] == 0:
                self.bestlap = (driver_name, timeInMs)
                return True
            else:
                if self.bestlap[1] > timeInMs:
                    self.bestlap = (driver_name, timeInMs)
                    return True
        return False

    def __writeSections(self, driver_name, sections) -> bool:
        result = False
        for i in range(3):
            if sections[i] > 0:
                if self.best_sections[i][1] == 0:
                    self.best_sections[i] = driver_name, sections[i]
                    result = True
                else:
                    if self.best_sections[i][1] > sections[i]:
                        self.best_sections[i] = driver_name, sections[i]
                        result = True
        return result
        
    
    def cmpAndWriteResults(self, driver_name, lap_timeInMs, sections) -> bool:
        result = self.__writeLap(driver_name, lap_timeInMs)
        if self.__writeSections(driver_name, sections):
            return True
        else:
            return result

    def getBestLapFormatted(self) -> tuple:
        utils.log("[Session] Running getBestLapFormatted()...")
        if self.bestlap[0] is not None:
            utils.log("[Session] Finishing getBestLapFormatted(): 1")
            return (self.bestlap[0], utils.formatTime(self.bestlap[1]))
        utils.log("[Session] Finishing getBestLapFormatted(): 2")
        return ("---", utils.formatTime(self.bestlap[1]))

    def getBestSectionFormatted(self, index) -> tuple:
        if index < 3:
            if self.best_sections[index][0] is not None:
                return (self.best_sections[index][0], utils.formatTime(self.best_sections[index][1]))
            return ("---", utils.formatTime(self.best_sections[index][1]))
        else:
            raise IndexError

    def getOptimalLapTimeFormatted(self) -> int:
        return utils.formatTime(self.best_sections[0][1] + self.best_sections[1][1] + self.best_sections[2][1])
