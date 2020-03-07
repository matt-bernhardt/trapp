# -*- coding: utf-8 -*-
from trapp.record import Record


class Venue(Record):

    def lookupID(self, data, log):
        # Check for required parameters
        required = ['VenueName']
        self.checkData(data, required)

        # see if any venue matches this name
        sql = ('SELECT ID '
               'FROM tbl_venues '
               'WHERE VenueName = %s')
        rs = self.db.query(sql, (data['VenueName'], ))
        if (rs.with_rows):
            records = rs.fetchall()
        venues = []
        for item in records:
            venues.append(item[0])

        # Return list of matched IDs
        return venues
