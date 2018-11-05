#!/usr/bin/python3
"""
Configuration setting like scoring constants, numbers of players, etc. for
ceiling game.  In this one, it's bowling-like, default 2 players, 10 turns,
scoring function is k/(dist + c)^r

Copyright 2018, David Lenkner
"""

from actions import ActionType
from typing import List


class CeilingGameConfig(object):
    """Class for ceiling game setup and scoring"""
    def __init__(self):
        """Set up with default params"""
        self.n_players = 2
        self.n_turns = 10
        self.k = 1
        self.c = 0.1
        self.r = 1

    def _score(self, distance):
        """Score a throw based on distance - max the throw can get"""
        return self.k * 1.0 / (distance + self.c) ** self.r

    def get_status_strings(self, events_distances: List[Tuple[str, float]]):
        """Get various status indicators on game, esp. scoring table and summary"""
        # First get list of turns and scores by player
        # Use knowledge of the void action strings in db (ActionType)
        # Score it. get summary strings,.  Return all
