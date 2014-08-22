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

from datetime import date, timedelta
from collections import Counter

def daterange(start_date, end_date):
    """Iterate over dates from start_date to end_date
    (exclusive of end_date as with Python range)"""
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def do_report(from_date:date, to_date:date, events:list):
    """ Produce a list of dicts, one for each day between from_date
        and to_date inclusive, where each dict has the key "date" that
        is a datetime.date object and one key for each flag with
        the count of flags on that date"""
    deltas = {d:Counter() for d in daterange(from_date, to_date + timedelta(1)) }
    prior = Counter()
    all_flags = set()
    for d, tick, flag in events:
        all_flags.add(flag)
        if d < from_date:
            prior[flag] += tick
        elif d <= to_date:
            deltas[d][flag] += tick

    # Convert deltas to absolute values and ensure all keys are present.
    report = []
    empty = dict.fromkeys(all_flags, 0)
    for d in daterange(from_date, to_date + timedelta(1)):
        prior = prior + deltas[d]
        current = dict(empty)
        current.update(prior)
        report.append(current)
    return report

if __name__ == '__main__':
    from events import RECORDS
    first, last = date(2014,7,27), date(2014, 8, 20)
    report = do_report(first, last, RECORDS)
    for d, row in zip(daterange(first, last), report):
        print(d, *list("{}:{}".format(flag, row[flag]) for flag in sorted(row)))
        