from datetime import datetime
import random

class Checksum:
    def generateMembershipId(db):
        traveller_id = ""
        while True:
            current_year = datetime.now().year
            current_year_short = str(current_year)[2:]

            traveller_id = current_year_short
            for i in range(0, 7):
                traveller_id += str(random.randint(0, 9))

            check_digit = sum(int(digit) for digit in traveller_id) % 10
            traveller_id += str(check_digit)
            if db.findTravellerID(traveller_id):
                pass
            else:
                break
            break
        return traveller_id
    
        