def calc_sessions_active_time(file_path):
    """Function to read the log file and calculate the no of sessions and total active time given requirements"""

    # context manager to read the logs of the log file
    with open(file_path) as f:
        lines = f.readlines()
    # empty dictionary to fill the data with name,sessions,activetime of user
    fair_bill_dict = {}
    # variable to save the first entry time of any user so we will this value in later part when we miss start time of any session
    TimeAtStartOfBill = None
    for eachLine in lines:
        # splitting the line into timestamp,name and start/end sessions
        time_stamp, name, begin_end = eachLine.split(" ")
        # convert the entire timestamp into seconds for computation
        time_in_secs = calculate_time(time_stamp)
        begin_end = begin_end.strip()
        # save the first time entry of the logfile
        if TimeAtStartOfBill is None:
            TimeAtStartOfBill = time_in_secs
        # check if the current entry is present as key in the fair_bill_dict
        if name in fair_bill_dict:
            # if present check whether it is start or end
            if begin_end == "Start":
                # increment the count of sessions for every start and append to starttimes list
                fair_bill_dict[name]["session_count"] += 1
                fair_bill_dict[name]["start_times"].append(time_in_secs)
            elif begin_end == "End":
                # if starttimes is empty but still end record is retrieved,increment the count sessions and calculate time as difference of current timestamp and time at the start of bill
                if len(fair_bill_dict[name]["start_times"]) == 0:
                    fair_bill_dict[name]["session_count"] += 1
                    fair_bill_dict[name]["total_time"] += (
                        time_in_secs - TimeAtStartOfBill
                    )
                else:
                    # calculate the time taken by differencing of time stamp and earlier starttime so referring to index 0 in start_times list
                    fair_bill_dict[name]["total_time"] += (
                        time_in_secs - fair_bill_dict[name]["start_times"][0]
                    )
                    # once time differencing is calculated,removing the corresponding start time
                    time_in_secs - fair_bill_dict[name]["start_times"].pop(0)
        else:
            # if name is the new entry of the fair_bill_dict,assign the values based on start/end
            if begin_end == "Start":
                fair_bill_dict[name] = {
                    "session_count": 1,
                    "start_times": [time_in_secs],
                    "total_time": 0,
                }
            elif begin_end == "End":
                fair_bill_dict[name] = {
                    "session_count": 1,
                    "start_times": [],
                    "total_time": time_in_secs - TimeAtStartOfBill,
                }
    # loop the fair_bill_dict and display the name,sessions_count and total active time of the user

    for key, value in fair_bill_dict.items():
        sessions = value["session_count"]
        total_time = value["total_time"]
        print(f"{key} {sessions} {total_time}")


def calculate_time(time_stamp):
    """function to convert the entire timestamp into seconds"""
    total_secs = 0
    hrs, mins, secs = time_stamp.split(":")
    total_secs += int(hrs) * 60 * 60
    total_secs += int(mins) * 60
    total_secs += int(secs)
    return total_secs


calc_sessions_active_time("logFile.txt")
