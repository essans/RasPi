#!/usr/bin/env python3

#load log file and convert to conventient dataframe

import json
import pandas as pd

jsonlist = []

with open("sysinfo.log") as logfile:

        for record in logfile:
                jsonlist.append(json.loads(record))

df_log = pd.DataFrame(jsonlist)

