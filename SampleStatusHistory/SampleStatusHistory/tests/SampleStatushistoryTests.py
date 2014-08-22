# Copyright (c) 2014, Duncan Booth
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided
# with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# "LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# "FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# "COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# "INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# "(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# "SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# "HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# "STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# "ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# "OF THE POSSIBILITY OF SUCH DAMAGE.
import unittest
from SampleStatusHistory import do_report
from datetime import date, timedelta

class SampleStatusHistoryTest_test1(unittest.TestCase):
    def test_null(self):
        """to_date before from_date returns empty list"""
        from_date = date(2014, 8, 2)
        to_date = date(2014, 8, 1)
        result = do_report(from_date, to_date, [])
        self.assertEqual(result, [])

    def test_no_events(self):
        """No events, but the resulting list should still have an entry for each date"""
        from_date = date(2014, 8, 2)
        to_date = from_date + timedelta(2)
        result = do_report(from_date, to_date, [])
        self.assertEqual(result, [{}, {}, {},])

    def test_single_event(self):
        """No events, but the resulting list should still have an entry for each date"""
        from_date = date(2014, 8, 1)
        to_date = from_date
        events =  [
            (date(2014,  8,  1),1,"DISPATCH"),
        ]
        result = do_report(from_date, to_date, events)
        self.assertEqual(result,
                        [{"DISPATCH":1}])

    def test_multi_events_one_day(self):
        """Still on one day so we don't have to aggregate days, but multiple events."""
        from_date = date(2014, 8, 1)
        to_date = from_date
        events =  [
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  8,  1),-1,"DISPATCH"),
            (date(2014,  8,  1),1,"WITH_CUSTOMER"),
        ]
        result = do_report(from_date, to_date, events)
        self.assertEqual(result,
                        [{"DISPATCH":2, "WITH_CUSTOMER":1}])

    def test_multi_events_two_days(self):
        """Aggregate results from previous day"""
        from_date = date(2014, 8, 1)
        to_date = from_date + timedelta(1)
        events =  [
            (date(2014,  8,  2),-1,"DISPATCH"),
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  8,  1),-1,"DISPATCH"),
            (date(2014,  8,  1),1,"WITH_CUSTOMER"),
            (date(2014,  8,  2),1,"WITH_CUSTOMER"),
        ]
        result = do_report(from_date, to_date, events)
        self.assertEqual(result,
                        [
                        {"DISPATCH":2, "WITH_CUSTOMER":1},
                        {"DISPATCH":1, "WITH_CUSTOMER":2},
                        ])

    def test_data_out_of_range(self):
        """Include data before start, ignore data after end"""
        from_date = date(2014, 8, 1)
        to_date = from_date + timedelta(1)
        events =  [
            (date(2014,  8,  2),-1,"DISPATCH"),
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  7,  31),1,"DISPATCH"),
            (date(2014,  8,  3),1,"DISPATCH"),
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  8,  1),-1,"DISPATCH"),
            (date(2014,  8,  1),1,"WITH_CUSTOMER"),
            (date(2014,  8,  2),1,"WITH_CUSTOMER"),
        ]
        result = do_report(from_date, to_date, events)
        self.assertEqual(result,
                        [
                         {"DISPATCH":2, "WITH_CUSTOMER":1},
                         {"DISPATCH":1, "WITH_CUSTOMER":2},
                        ])

    def test_all_flags_exist(self):
        """Aggregate results from previous day"""
        from_date = date(2014, 8, 1)
        to_date = from_date + timedelta(1)
        events =  [
            (date(2014,  8,  2),-1,"DISPATCH"),
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  8,  1),1,"DISPATCH"),
            (date(2014,  8,  1),-1,"DISPATCH"),
            (date(2014,  8,  1),1,"WITH_CUSTOMER"),
            (date(2014,  8,  2),1,"WITH_CUSTOMER"),
            (date(2014,  8,  2),1,"EXTRACT"),
            (date(2014,  7,  2),1,"RECEIPT_EMAIL"),
            (date(2014,  7,  2),-1,"RECEIPT_EMAIL"),
        ]
        result = do_report(from_date, to_date, events)
        self.assertEqual(result,
                        [
                        {"DISPATCH":2, "WITH_CUSTOMER":1, "EXTRACT":0, "RECEIPT_EMAIL":0},
                        {"DISPATCH":1, "WITH_CUSTOMER":2, "EXTRACT":1, "RECEIPT_EMAIL":0},
                        ])


if __name__ == '__main__':
    unittest.main()
