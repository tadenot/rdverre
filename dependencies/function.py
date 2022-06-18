from typing import List
import h3
import numpy as np

from parameters import *
import google_api as google


class Location:
    def __init__(self, lat: float, lng: float) -> None:
        self.lat = lat
        self.lng = lng

    def to_string(self):
        return f"{self.lat},{self.lng}"


class Gadjo:
    def __init__(self, name: str, location: Location) -> None:
        self.name = name
        self.location = location


class GadjosTeam:
    def __init__(self, gadjos: List[Gadjo]) -> None:
        self.gadjos = gadjos

    def distance_center(self) -> Location:
        x_avg = 0
        y_avg = 0
        z_avg = 0
        for gadjo in self.gadjos:
            lat_rad = gadjo.location.lat * np.pi / 180
            lng_rad = gadjo.location.lng * np.pi / 180
            x_avg += np.cos(lat_rad) * np.cos(lng_rad)
            y_avg += np.cos(lat_rad) * np.sin(lng_rad)
            z_avg += np.sin(lat_rad)

        x_avg /= len(self.gadjos)
        y_avg /= len(self.gadjos)
        z_avg /= len(self.gadjos)

        lng_avg = np.arctan2(y_avg, x_avg)
        hyp_avg = np.sqrt(x_avg * x_avg + y_avg * y_avg)
        lat_avg = np.arctan2(z_avg, hyp_avg)

        return Location(lat_avg * 180 / np.pi, lng_avg * 180 / np.pi)

    def score_meet_up(self, meet_up: Location) -> float:
        distance_matrix = google.distance_matrix(
            [meet_up], [gadjo.location for gadjo in self.gadjos]
        )
        score = 0
        for row in distance_matrix["rows"]:
            score += int(row["elements"][0]["duration"]["value"])
        return score / len(self.gadjos)

    def find_best_meet_up(self) -> Location:

        distance_center = self.distance_center()
        center_hex = h3.geo_to_h3(
            distance_center.lat, distance_center.lng, H3_RESOLUTION
        )
        viewed_hex = {center_hex: 1}
        while True:
            pass
        pass
