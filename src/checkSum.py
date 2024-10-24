from datetime import datetime
import random

class Checksum:
    def generateMembershipId(db):
        membership_id = ""
        while True:
            current_year = datetime.now().year
            current_year_short = str(current_year)[2:]

            membership_id = current_year_short
            for i in range(0, 7):
                membership_id += str(random.randint(0, 9))

            check_digit = sum(int(digit) for digit in membership_id) % 10
            membership_id += str(check_digit)
            if db.findMembershipID(membership_id):
                pass
            else:
                break
            break
        return membership_id
    
        