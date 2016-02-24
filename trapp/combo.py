# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.record import Record


class Combo(Record):

    # Combos are groups of teammates, recorded as one entry for analysis.
    # Combos of two players can be one of four options:
    # 1) Both players on the field
    # 2) Both players off the field
    # 3) Player A without Player B
    # 4) Player B without Player A
    # Eventually these may be expanded to arbitrary sized groupings.

    def lookupID(self, player1, player2):
        if not (isinstance(player1, int) and isinstance(player2, int)):
            raise RuntimeError('lookupID requires two integers')

        sql = ('SELECT c.ID '
               'FROM lnk_players_combos l1 '
               'INNER JOIN tbl_combos c ON l1.ComboID = c.ID '
               'INNER JOIN lnk_players_combos l2 ON c.ID = l2.ComboID '
               'WHERE l1.PlayerID = %s AND l2.PlayerID = %s')
        rs = self.db.query(sql, (player1, player2, ))
        if (rs.with_rows):
            records = rs.fetchall()

        data = []

        for term in records:
            data.append(term[0])

        return data
