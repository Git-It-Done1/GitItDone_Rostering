from .strategy import *



class EvenDistribution(ScheduleStrategy):

    def distribute_shifts(self, staff, shifts, week_start=None):
        assignments = {}

        if not staff:
            return Schedule(assignments)
        

        staff_ids = [get_staff_id(member) for member in staff]
        for staff_id in staff_ids:
            assignments[staff_id] = []
        
        i = 0
        num_staff = len(staff_ids)
        
        for shift in shifts:
            staff_id = staff_ids[i % num_staff]
            assignments[staff_id].append(shift)
            i += 1
        
        return Schedule(assignments)
    
# This use an even distribution, a round robin approach, to assign shifts to staff members in order. - VR