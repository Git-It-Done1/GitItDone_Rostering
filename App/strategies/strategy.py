from abc import ABC, abstractmethod

class Schedule:
    def __init__(self, assignments):
        if assignments is not None:
            self.assignments = assignments
        else:
            self.assignments = {}

    def to_dict(self):
        out = {}
        for shiftID, shifts in self.assignments.items():
            out[shiftID] = []
            for item in shifts:
                if isinstance(item, dict):
                    out[shiftID].append(item)
                elif hasattr(item, "get_json"):
                    out[shiftID].append(item.get_json())
                else:
                    out[shiftID].append(str(item))
        return out
    
class ScheduleStrategy(ABC):
    @abstractmethod
    def distribute_shifts(self, staff, shifts, week_start=None):
        raise NotImplementedError("distribute_shifts must be implemented by subclasses")
        

def get_staff_id(staff_member):
    if staff_member is None:
        raise ValueError("Staff member cannot be None")
    
    if isinstance(staff_member, dict):
        if "id" in staff_member and staff_member["id"] is not None:
            return str(staff_member["id"])
    else:
        val = getattr(staff_member, "id", None)
        if val is not None:
            return str(val)
    
    raise ValueError("Unable to determine staff member ID") 
                

def get_shift_day(shift):
    if shift is None:
        return None
    
    if isinstance(shift, dict):
        st = shift.get("start_time")
    else:
        st = getattr(shift, "start_time", None)
    
    if st is not None:
        if hasattr(st, "date"):
            return st.date()
        if hasattr(st, "strftime"):
            return st.strftime("%Y-%m-%d")
        if isinstance(st, str):
            return st.split("T")[0]
    
    return None


def get_shift_type(shift):
    if shift is None:
        return "day"
    
    if isinstance(shift, dict):
        startTime = shift.get("start_time")
    else:
        startTime = getattr(shift, "start_time", None)

    if startTime is not None:
        if hasattr(startTime, "hour"):
            hour = startTime.hour
            if (hour >= 18 or hour < 6):
                return "night"
            else:
                return "day"
        
        if isinstance(startTime, str):
            try:
                if "T" in startTime:
                    timePart = startTime.split("T")[1]
                    hour = int(timePart.split(":")[0])
                else:
                    hour = int(startTime.split(":")[0])
                if (hour >= 18 or hour < 6):
                    return "night"
                else:
                    return "day"
                
            except Exception:  
                return "day"
            
    return "day"


def get_shift_id(shift):
    if shift is None:
        return None

    if isinstance(shift, dict):
        if "id" in shift and shift["id"] is not None:
            return shift["id"]
    else:
        val = getattr(shift, "id", None)
        if val is not None:
            return val
    return None