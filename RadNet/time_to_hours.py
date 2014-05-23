__author__ = 'Joshua Moravec'
"""
This function converts a time string of HHMMSS to hours past midnight
"""


def time_to_hours(time_string):
    time_string = str(time_string)
    time = float(time_string[0:2]) + \
        float(time_string[2:4])/60.0 + \
        float(time_string[4:6])/3600.0
    return time