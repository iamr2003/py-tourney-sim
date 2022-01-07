import random
import numpy
import functools

#attributes will be modeled as a range via gaussian distribution, where 99% of values fall between bounds(aka 2.58 stdevs)
#because state is cached in structures, calling some methods multiple times can lead to bad things

def randNormal(bound = []):
    #written for explicitness, yes less mem efficient
    min = bound[0]
    max = bound[1]
    if(min == max):
        return min
    mean = (max+min)/2
    stdev = (max - mean)/2.58 #99% bound, could be a bit bigger if needed

    #all int things in the end
    return round(numpy.random.normal(mean,stdev))

class boundGen:
    #bounds on the generation of generators per team, aka how low/high the averages can go
    def __init__(self,minMin,minMax,maxMin,maxMax) -> None:
        self.min = [minMin,minMax]
        self.max = [maxMin,maxMax]

#a team who always plays exactly the same
class teamStatic:
    def __init__(self,staticAttr ={}) -> None:
        self.attr = staticAttr
    def play(self):
        return self.attr

#a team whose performance varies between matches
class teamReal:
    def __init__(self,number = 0,attrGen = {}) -> None:
        self.number = number
        self.attrBounds = {}
        self.generateAttrs(attrGen)
    
    def generateAttrs(self,attrGen = {}):
        for k , v in attrGen.items():
            self.attrBounds[k] = [randNormal(v.min),randNormal(v.max)]

    def play(self):
        attr = {}
        for k,v in self.attrBounds:
            attr[k] = randNormal(v)
        return attr

#rules is a dictionary to functions, where the function scores the rule
def scoreAttrs(attrs,rules):
    attrScore = {}
    #basically a map, but I don't like python fp tools
    for k,v in rules:
        attrScore[k] += v(attrs[k])
    return attrScore

# gah proper maps/folds would clean up much of this
class alliance:
    def __init__(self,teams = []) -> None:
        self.teams = teams
    def play(self):
        self.result = []
        for team in self.teams:
            self.result.append(team.play())
        self.total()
        self.score()

    def total(self):
        self.comboResult = {}
        for dict in self.result:
            for k , v in dict:
                self.comboResult[k] += v

    def score(self,rules):    
        self.scoredResult = scoreAttrs(self.comboResult,rules)
        for k , v in self.scoredResult:
            self.total += v

class match:
    def __init__(self,red = alliance,blue = alliance) -> None:
        self.red = red
        self.blue = blue
        # to be used in scheduler/ranker
        self.surrogates = []
    def play(self):
        self.red.play()
        self.blue.play()

class schedule:
    def __init__(self,teamSet={}) -> None:
        self.teamSet = teamSet
        self.matches = []

    def gen_matches(self, n):
        #will deal with surrogates later
        while(n>0):
            teamList = list(self.teamSet)
            random.shuffle(teamList)
            while(len(teamList) >= 6):
                red = alliance([teamList.pop(0),teamList.pop(0),teamList.pop(0)])
                blue = alliance([teamList.pop(0),teamList.pop(0),teamList.pop(0)])
                self.matches.append(match(red,blue))
                n = n-1

#gah need to write a quick ranker
#do some light testing, write a short demo program

                
