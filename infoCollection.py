import re, validators


def basicInfo():
    channels = []
    decision: str = None
    loopBreaker: bool = None
    while True:
        if loopBreaker != True:
            channel = input("Please, provide the handle (@youtuber) found on the page of the YouTube channel you want to examin\n")
            if handleTester(channel) == False:
                continue
            else:
                channels.append(channel)
                while True:
                    if (decision != "no"):
                        decision = input("Are there any more channels you want to examin? (Yes/No)\n").lower()
                        if decision == "yes":
                            break
                        elif decision not in ["no", "yes"]:
                            print("Please provide an answer in the right format")
                            continue
                    elif (decision == "no"):
                        loopBreaker = True
                        break
        elif loopBreaker == True:
            break
    return channels


def handleTester(handle: str):
    if validators.url(handle) == True:
        print("Insert a valid handle")
        return False
    match = re.match(r"^(?=.{3,30}$)\@[A-Za-z0-9][\w\-.·]*[A-Za-z0-9]$", handle)
    if match == None:
        print("Insert a valid handle")
        return False
    else: 
        return True
