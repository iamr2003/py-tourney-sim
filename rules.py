#this section utilizes a lot of things that return functions
#if doesn't make sense to you, look into "function currying" to understand better


#rules is a dictionary to functions, where the function scores the rule
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
