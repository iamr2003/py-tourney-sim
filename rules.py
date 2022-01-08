#this section utilizes a lot of things that return functions
#if doesn't make sense to you, look into "function currying" to understand better


#rules is a dictionary to functions, where the function scores the rule
from typing import MutableMapping
from sim import teamReal

def scoreAttrs(attrs,rules):
    attrScore = {}
    #basically a map, but I don't like python fp tools
    for k,v in rules.items():
        if k in attrs:
            if k in attrScore:
                attrScore[k] = v(attrs[k]) + attrScore[k]
            else:
                attrScore[k] = v(attrs[k])
    return attrScore

#for any situation where scoring is only dependent on each team's performance individually summed
#aka, no situations where multiple robots must be together in scoring(balancing, etc.)
def basicScorer(rules):
    def scorer(teamResults):
        total = 0
        for result in teamResults:
            for k, v in scoreAttrs(result,rules).items():
                total += v
        return total
    return scorer

#returns a function that multiplies by a value
def mult(a):
    def y(x):
        return a*x
    return y



#IRSIMPLE
#just shots and climbs

#1 is park, 2 is hang
def IRclimbSimple(nClimbs):
    if(nClimbs == 2):
        return 25
    elif(nClimbs == 1):
        return 5
    else:
        return 0

infRechargeSimple = {
    "innerGoals":mult(3),
    "outerGoals":mult(2),
    "climbs":IRclimbSimple
}

#I'd like to generalize a bit more, but we'll see
#the repeated patterns here are rough
#gah dict defaults are annoying
#next step would be to abstract out RP defs, but this will be fine for now

def IRSimpleRanker(matchList,teamSet):
    rankinfo = {}
    for match in matchList:
        #total matches
        for alliance in [match.red,match.blue]:
                for team in alliance.teams:
                    if team.number in rankinfo:
                        if "n" in rankinfo[team.number]:
                            rankinfo[team.number]["n"] += 1
                        else:
                            rankinfo[team.number]["n"] = 1
                    else:
                        rankinfo[team.number] = {"n":1}
        #WP
        if match.winner == "red" or match.winner == "blue":
            if match.winner == "red":
                winner = match.red
            else:
                winner = match.blue
            for team in winner.teams:
                if team.number in rankinfo:
                    if "RP" in rankinfo[team.number]:
                        rankinfo[team.number]["RP"] += 2
                    else:
                        rankinfo[team.number]["RP"] = 2
                else:
                    rankinfo[team.number] = {"RP":2}
        else:
            for alliance in [match.red,match.blue]:
                for team in alliance.teams:
                    if team.number in rankinfo:
                        if "RP" in rankinfo[team.number]:
                            rankinfo[team.number]["RP"] += 1
                        else:
                            rankinfo[team.number]["RP"] = 1
                    else:
                        rankinfo[team.number] = {"RP":1}
        #RP
        for alliance in [match.red,match.blue]:
            #say 2 climbs 1 park for RP and 49 balls for RP
            totalBalls = alliance.comboResult["innerGoals"] + alliance.comboResult["outerGoals"]
            if totalBalls >= 49:
                for team in alliance.teams:
                    if team.number in rankinfo:
                        if "RP" in rankinfo[team.number]:
                            rankinfo[team.number]["RP"] += 1
                        else:
                            rankinfo[team.number]["RP"] = 1
                    else:
                        rankinfo[team.number].append({"RP":1})
            if alliance.comboResult["climbs"]>=5:
                for team in alliance.teams:
                    if team.number in rankinfo:
                        if "RP" in rankinfo[team.number]:
                            rankinfo[team.number]["RP"] += 1
                        else:
                            rankinfo[team.number]["RP"] = 1
                    else:
                        rankinfo[team.number] = {"RP":1}

    # need to figure how to sort my multiple keys
    def aveRP(n1): 
        if n1.number in rankinfo and "RP" in rankinfo[n1.number] and "n"  in rankinfo[n1.number]:
            return rankinfo[n1.number]["RP"]/rankinfo[n1.number]["n"]
        else:
            return 0

    teamList = list(teamSet)
    ranking = sorted(teamList,key = aveRP)
    return ranking

#RAPID REACT FULL RULESET

#require python 3.10
#climbs 0,1,2,3,4 - none,low,mid,high, trav
def RRclimb(state):
    pts = {
        0:0,
        1:4,
        2:6,
        3:10,
        4:15
    }
    return pts[state]


RR = {
    "taxi":mult(2),
    "autoLower":mult(2),
    "autoUpper":mult(4),
    "teleopLower":mult(1),
    "teleopUpper":mult(2),
    "climbs":RRclimb
}

def RR_ranker(matchList,teamSet):
    rankinfo = {}
    for match in matchList:
        #total matches
        for alliance in [match.red,match.blue]:
                for team in alliance.teams:
                    if team.number in rankinfo:
                        if "n" in rankinfo[team.number]:
                            rankinfo[team.number]["n"] += 1
                        else:
                            rankinfo[team.number]["n"] = 1
                    else:
                        rankinfo[team.number] = {"n":1}
        #WP
        if match.winner == "red" or match.winner == "blue":
            if match.winner == "red":
                winner = match.red
            else:
                winner = match.blue
            for team in winner.teams:
                if team.number in rankinfo:
                    if "RP" in rankinfo[team.number]:
                        rankinfo[team.number]["RP"] += 2
                    else:
                        rankinfo[team.number]["RP"] = 2
                else:
                    rankinfo[team.number] = {"RP":2}
        else:
            for alliance in [match.red,match.blue]:
                for team in alliance.teams:
                    if team.number in rankinfo:
                        if "RP" in rankinfo[team.number]:
                            rankinfo[team.number]["RP"] += 1
                        else:
                            rankinfo[team.number]["RP"] = 1
                    else:
                        rankinfo[team.number] = {"RP":1}
        #RP
        for alliance in [match.red,match.blue]:
            #climb pts >= 15
            climbpts = 0
            autoBalls = 0
            totalBalls = 0
            for result in alliance.result:
                climbpts += RRclimb(result["climbs"])
                autoBalls += result["autoLower"] + result["autoUpper"]
                totalBalls += result["autoLower"] + result["autoUpper"] + result["teleopLower"] + result["teleopUpper"]

            if climbpts >= 15:
                for team in alliance.teams:
                    if team.number in rankinfo:
                        if "RP" in rankinfo[team.number]:
                            rankinfo[team.number]["RP"] += 1
                        else:
                            rankinfo[team.number]["RP"] = 1
                    else:
                        rankinfo[team.number].append({"RP":1})

            if autoBalls >=5:
                ballsNeeded = 18
            else:
                ballsNeeded = 20

            if totalBalls >= ballsNeeded:
                for team in alliance.teams:
                    if team.number in rankinfo:
                        if "RP" in rankinfo[team.number]:
                            rankinfo[team.number]["RP"] += 1
                        else:
                            rankinfo[team.number]["RP"] = 1
                    else:
                        rankinfo[team.number] = {"RP":1}

    # need to figure how to sort my multiple keys
    def aveRP(n1): 
        if n1.number in rankinfo and "RP" in rankinfo[n1.number] and "n"  in rankinfo[n1.number]:
            return rankinfo[n1.number]["RP"]/rankinfo[n1.number]["n"]
        else:
            return 0

    teamList = list(teamSet)
    ranking = sorted(teamList,key = aveRP)
    return ranking