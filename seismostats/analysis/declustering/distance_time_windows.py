# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
# LICENSE
#
# Copyright (C) 2010-2023 GEM Foundation, G. Weatherill, M. Pagani,
# D. Monelli.
#
# The Hazard Modeller's Toolkit is free software: you can redistribute
# it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>
#
# DISCLAIMER
#
# The software Hazard Modeller's Toolkit (openquake.hmtk) provided herein
# is released as a prototype implementation on behalf of
# scientists and engineers working within the GEM Foundation (Global
# Earthquake Model).
#
# It is distributed for the purpose of open collaboration and in the
# hope that it will be useful to the scientific, engineering, disaster
# risk and software design communities.
#
# The software is NOT distributed as part of GEM’s OpenQuake suite
# (https://www.globalquakemodel.org/tools-products) and must be considered as a
# separate entity. The software provided herein is designed and implemented
# by scientific staff. It is not developed to the design standards, nor
# subject to same level of critical review by professional software
# developers, as GEM’s OpenQuake software suite.
#
# Feedback and contribution to the software is welcome, and can be
# directed to the hazard scientific staff of the GEM Model Facility
# (hazard@globalquakemodel.org).
#
# The Hazard Modeller's Toolkit (openquake.hmtk) is therefore distributed
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# The GEM Foundation, and the authors of the software, assume no
# liability for use of the software.
import abc
import numpy as np
import pandas as pd


DistanceTimeWindow = tuple[np.ndarray[float], np.ndarray[pd.Timedelta]]
_DistanceTimeWindow = tuple[np.ndarray[float], np.ndarray[float]]


class BaseDistanceTimeWindow(abc.ABC):
    """
    Defines the space and time windows, within which an event is identified
    as a cluster.
    """

    def __init__(self, time_cutoff: float | None = None):
        """
        Args:
            time_cutoff: time window cutoff in days (optional).
                No time windows larger than time_cutoff are returned.
        """
        self.time_cutoff = time_cutoff

    @abc.abstractmethod
    def _calc(self, magnitude: np.ndarray,
              ) -> _DistanceTimeWindow:
        """
        Calculate the space and time windows for given magnitudes

        Args:
            magnitude: array of magnitudes

        Returns:
            sw_space: array of space windows in km
            sw_time: array of time windows as decimal days
        """
        return NotImplemented

    def __call__(self, magnitude: np.ndarray):
        """
        Calculate the space and time windows for given magnitudes with cutoff

        Args:
            magnitude: array of magnitudes

        Returns:
            sw_space: array of space windows in km
            sw_time: array of time windows
        """
        sw_space, sw_time = self._calc(magnitude)
        if self.time_cutoff:
            sw_time = np.clip(sw_time, a_min=0, a_max=self.time_cutoff)
        sw_time = np.array([pd.Timedelta(days=t) for t in sw_time])
        return sw_space, sw_time


class GardnerKnopoffWindow(BaseDistanceTimeWindow):
    """
    Gardner Knopoff method for calculating distance and time windows

    Source:
        Gardner and Knopoff, 1974
    """

    def _calc(self, magnitude: np.ndarray) -> _DistanceTimeWindow:
        sw_space = np.power(10.0, 0.1238 * magnitude + 0.983)
        sw_time = np.power(10.0, 0.032 * magnitude + 2.7389)
        sw_time[magnitude < 6.5] = (
            np.power(10.0, 0.5409 * magnitude[magnitude < 6.5] - 0.547)
        )
        return sw_space, sw_time


class GruenthalWindow(BaseDistanceTimeWindow):
    """
    Gruenthal method for calculating distance and time windows

    Source:
        Gruenthal, 1985; see van Stiphout et al., 2012
    """

    def _calc(self, magnitude: np.ndarray) -> _DistanceTimeWindow:
        sw_space = np.exp(1.77 + np.sqrt(0.037 + 1.02 * magnitude))
        sw_time = np.abs(
            (np.exp(-3.95 + np.sqrt(0.62 + 17.32 * magnitude)))
        )
        sw_time[magnitude >= 6.5] = (
            np.power(10, 2.8 + 0.024 * magnitude[magnitude >= 6.5])
        )
        return sw_space, sw_time


class UhrhammerWindow(BaseDistanceTimeWindow):
    """
    Uhrhammer method for calculating distance and time windows

    Source:
        Uhrhammer, 1986
    """

    def _calc(self, magnitude: np.ndarray) -> _DistanceTimeWindow:
        sw_space = np.exp(-1.024 + 0.804 * magnitude)
        sw_time = np.exp(-2.87 + 1.235 * magnitude)
        return sw_space, sw_time
