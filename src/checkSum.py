from datetime import datetime
import random

class Checksum:
    def GenerateTravellerID(db):
        travellerID = ""
        while True:
            currentYear = datetime.now().year
            currentYearShort = str(currentYear)[2:]

            travellerID = currentYearShort
            for i in range(0, 7):
                travellerID += str(random.randint(0, 9))

            checkDigit = sum(int(digit) for digit in travellerID) % 10
            travellerID += str(checkDigit)
            if db.FindTravellerID(travellerID):
                pass
            else:
                break
            break
        return travellerID
    
        