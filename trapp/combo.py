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

    def lookupCombos(self, player1, player2):
        if not (isinstance(player1, int) and isinstance(player2, int)):
            raise RuntimeError('lookupID requires two integers')

        sql = ('SELECT c.ID, '
               '  l1.PlayerID AS Player1, l1.Exclude AS Exclude1, '
               '  l2.PlayerID AS Player2, l2.Exclude AS Exclude2 '
               'FROM lnk_players_combos l1 '
               'INNER JOIN tbl_combos c ON l1.ComboID = c.ID '
               'INNER JOIN lnk_players_combos l2 ON c.ID = l2.ComboID '
               'WHERE l1.PlayerID = %s AND l2.PlayerID = %s')
        rs = self.db.query(sql, (player1, player2, ))
        if (rs.with_rows):
            records = rs.fetchall()

        data = []

        for term in records:
            combo = {
                'ComboID': term[0],
                'Player1': term[1],
                'Exclude1': term[2],
                'Player2': term[3],
                'Exclude2': term[4]
            }
            data.append(combo)

        return data

    def registerCombo(self, player1, player2):
        # This creates the necessary database records for a player combo

        if not (isinstance(player1, int) and isinstance(player2, int)):
            raise RuntimeError('lookupID requires two integers')

        # Both
        exclude1 = 0
        exclude2 = 0
        self.saveCombo(player1, exclude1, player2, exclude2)

        # Neither
        exclude1 = 1
        exclude2 = 1
        self.saveCombo(player1, exclude1, player2, exclude2)

        # One
        exclude1 = 0
        exclude2 = 1
        self.saveCombo(player1, exclude1, player2, exclude2)

        # The Other
        exclude1 = 1
        exclude2 = 0
        self.saveCombo(player1, exclude1, player2, exclude2)

    def saveCombo(self, player1, exclude1, player2, exclude2):
        sql = ('INSERT INTO tbl_combos '
               '(Description) '
               'VALUES '
               '(%s)')
        rs = self.db.query(sql, (
            player1 + '_' + exclude1 + ',' + player2 + '_' + exclude2
        ))
