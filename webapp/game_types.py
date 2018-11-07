#!/usr/bin/python3
"""
Configuration setting like scoring constants, numbers of players, etc. for
ceiling game.  In this one, it's bowling-like, default 2 players, 10 turns,
scoring function is k/(dist + c)^r

Copyright 2018, David Lenkner
"""

from actions import ActionType
from database_utils import get_database_cnx
from typing import List, Tuple


class BowlingBase(object):
    """Class for ceiling game setup and scoring"""

    def __init__(self):
        """Set up with default params, can override"""
        self.n_players = 2
        self.n_turns = 3
        self.k = 1
        self.c = 0.1
        self.r = 1

    def _score(self, distance):
        """Score a throw based on distance - max the throw can get"""
        return self.k * 1.0 / (distance + self.c) ** self.r

    def _get_events_distances(self) -> List[Tuple[str, float]]:
        """Query database tables and join for turns/actions and scores corresponding"""
        squery = '''
            set @lt=NULL;
            select event_idx, event_type, min(b.distance) as min_d from
            (
                SELECT @rn:=@rn+1 as event_idx, `t`, @lt last_t, @lt:=t curr_t, `event_type`
                from (
                    select `t`, `event_type` FROM `events`
                    order by `t`
                ) t1, (SELECT @rn:=-1) t2
            ) as a
            inner join distances as b
                on b.t > a.last_t
                and b.t < a.curr_t
            group by event_idx;
	'''
        cnx = get_database_cnx()
        cursor = cnx.cursor()
        results = cursor.execute(squery, multi=True)
        for idx, result in enumerate(results):
            if idx == 1:
                events_distances = result.fetchall()
        cnx.close()
        return events_distances

    def get_status(self):
        """Get various status indicators on game, esp. scoring table and summary"""
        # First get list of turns and scores by player
        events_distances = self._get_events_distances()
        scores_byevent = [_score(x[2]) if (x[1] == ActionType.COMMIT_TURN_SCORE
                                           or x[1] == ActionType.START_GAME)
                          else 0.0 for x in events_distances]

        # Total score, get summary strings, table.  Bulk of work here. For each event
        scores_byplayer = [0.0 for i in range(self.n_players)]
        scores_byturn_byplayer = [['-' for j in range(self.n_players)] for i in range(self.n_turns)]
        for (idx, event_type, min_d) in events_distances:
            # Sum up scores per player, build display table
            turn_i, player_i = divmod((idx - 1), self.n_player)
            # Scores multiply with prev turn
            total_thisturn = scores_byevent[idx - 1]
            if turn_i >= 1:
                idx_last = idx - 1 - self.n_players
                total_thisturn *= scores_byevent[idx_last]
            # Record stuff for this turn
            scores_byplayer[player_i] += total_thisturn
            scores_byturn_byplayer[turn_i][player_i] = str(total_thisturn)

        # Return info in a dict
        return scores_byturn_byplayer, scores_byplayer


class BowlingTwoPlayer(BowlingBase):
    """Two players, 10 turns"""

    def __init__(self):
        super().__init__()
        self.n_players = 2
        self.n_turns = 10
