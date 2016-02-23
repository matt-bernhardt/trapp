# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time
from trapp.compiler import Compiler
from trapp.season import Season


class CompilerTeammates(Compiler):

    def doCompile(self):

        # First, we get a list of team-seasons recorded in the data
        s = Season()
        s.connectDB()
        self.seasons = s.loadAll()

        # Second, for each team-season:
        for item in self.seasons:

            print(str(item))
            self.log.message(str(item))

            # Get the list of players to have appeared in this season

            # Iterate over the list of players, building player pairs

            # Make sure each pair is recorded initially

            # Build data for each pair

            # Store data for each pair

        return True
