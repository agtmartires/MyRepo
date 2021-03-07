# Function SetSchedule() Will set schedule with parameters:
#  - Array of days when the task will run
#  - Time when the task will run on the specified days
#  - Date and time when the schedule will start
# Example: 
#  - Monday, Wednesday, Friday
#  - 9:00 AM
#  - March 1, 2021 9:00 PM
#
# This means that the scheduled task will be run at 9:00 AM every Monday, 
# Wednesday and Friday starting from June 22, 2020 9:00 PM.
#
# Function QueryDateTime() will accept a date_time as parameters: 
#  - March 1, 2021 9:00 AM
# This will check the input date and time against the set schedule and show:
#  - Prev Schedule    : previous date/time when the scheduled task should have run 
#  - Is scheduled now : whether the task should be run on the specified date/time 
#  - Next Schedule    : the next date/time when the scheduled task would be run 
# Example:
#  - Prev Schedule    : NONE
#  - Is scheduled now : NO
#  - Next Schedule    : March 3, 2021 9:00 AM 
# 

from datetime import datetime, timedelta
import time

sched = None

class Schedule:
    def __init__(self):
        self.days_of_week = []
        self.time_sched = None
        self.start_schedule = None

# Function to set start schedule
def SetSchedule(days_of_week, time_sched, start_sched):
    print("\n\nSCHED: " + start_sched)
    print("SCHED: " + days_of_week)
    print("SCHED: " + time_sched)
    global sched
    sched = Schedule()
    days_of_week = days_of_week.replace(" ", "")
    dow_list = days_of_week.split(",")

    try:
        for i in dow_list:
            sched.days_of_week.append(time.strptime(i,"%A").tm_wday)
    except ValueError:
        print("Invalid days of week input")
        return

    try:
        sched.time_sched = datetime.strptime(time_sched, "%I:%M %p")
    except ValueError:
        print("Invalid time schedule input")
        return

    try:
        sched.start_schedule = datetime.strptime(start_sched, "%B %d, %Y %I:%M %p")
    except ValueError:
        print("Invalid start schedule input")
        return


def GetPrevDay(sched, query_dt):
    result_dt = None
    if (query_dt <= sched.start_schedule):
        return None
    else:
        result_dt = query_dt

    for i in range(7):
        result_dt = result_dt + timedelta(days=-1)
        if (result_dt.timetuple()[6] in sched.days_of_week):
            break

    result_dt = datetime.combine(result_dt.date(), sched.time_sched.time())
    if (result_dt < query_dt and result_dt >= sched.start_schedule):
        return result_dt
    else:
        return None


def CheckLastSchedule(query_dt):
    last_sched = GetPrevDay(sched, query_dt)
    if (last_sched is None):
        print("  Prev Schedule     : NONE")
    else:
        print("  Prev Schedule     : " + last_sched.strftime("%B %d, %Y %I:%M %p"))


def CheckIfScheduled(query_dt):
    if ((query_dt.timetuple()[6] in sched.days_of_week) and
            query_dt >= sched.start_schedule and
            query_dt.time() == sched.time_sched.time()):
        print("  Is scheduled now  : YES")
    else:
        print("  Is scheduled now  : NO")


def GetNextDay(sched, query_dt):
    result_dt = None
    if (query_dt >= sched.start_schedule):
        result_dt = query_dt
    else:
        result_dt = sched.start_schedule

    for i in range(7):
        result_dt = result_dt + timedelta(days=1)
        if (result_dt.timetuple()[6] in sched.days_of_week):
            break

    result_dt = datetime.combine(result_dt.date(), sched.time_sched.time())
    return result_dt


def CheckNextSchedule(query_dt):
    next_sched = GetNextDay(sched, query_dt)
    print("  Next Schedule     : " + next_sched.strftime("%B %d, %Y %I:%M %p"))


# Function to get query date
def QueryDateTime(query_sched):
    print("----------------------------------------------")
    print("QUERY: " + query_sched)

    if (sched is None):
        print("Please set schedule first.")
        return

    try:
        query_dt = datetime.strptime(query_sched, "%B %d, %Y %I:%M %p")
        CheckLastSchedule(query_dt)
        CheckIfScheduled(query_dt)
        CheckNextSchedule(query_dt)
    except ValueError:
        print("Invalid query date/time input")
        return


if __name__ == '__main__':
    SetSchedule(
        "Monday, Wednesday, Friday",
        "9:00 AM",
        "March 1, 2021 9:00 PM"
    )
    QueryDateTime("March 1, 2021 9:00 AM")

