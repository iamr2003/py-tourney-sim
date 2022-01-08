import random
import numpy

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
    def __init__(self,number = 0,staticAttr ={}) -> None:
        self.number = number        
        self.attr = staticAttr
    def play(self):
        return self.attr

#a team whose performance varies between matches
class teamReal:
    #if you want to initialize gen directly, just assign it
    def __init__(self,number = 0,attrGen = {}) -> None:
        self.number = number
        self.attrBounds = {}
        self.generateAttrs(attrGen)
    
    def generateAttrs(self,attrGen = {}):
        for k , v in attrGen.items():
            self.attrBounds[k] = [randNormal(v.min),randNormal(v.max)]

    def play(self):
        attr = {}
        for k,v in self.attrBounds.items():
            attr[k] = randNormal(v)
        return attr

# gah proper maps/folds would clean up much of this
class alliance:
    def __init__(self,teams = []) -> None:
        self.teams = teams
    def play(self):
        self.result = []
        for team in self.teams:
            self.result.append(team.play())
        self.mergeResults()

    def mergeResults(self):
        self.comboResult = {}
        for dict in self.result:
            for k , v in dict.items():
                if k in self.comboResult:
                    self.comboResult[k] += v
                else:
                    self.comboResult[k] = v

    def score(self,scorer):
        #allows for lots of flexibility in scoring
        self.total =  scorer(self.result)

    def str(self):
        o_str = ""
        for t in self.teams:
            o_str = o_str + " " + str(t.number)
        return o_str

class match:
    def __init__(self,red = alliance,blue = alliance) -> None:
        self.red = red
        self.blue = blue
        # to be used in scheduler/ranker
        self.surrogates = []
    def play(self,scorer):
        self.red.play()
        self.red.score(scorer)
        self.blue.play()
        self.blue.score(scorer)
        if(self.red.total > self.blue.total):
            self.winner = "red"
        elif(self.red.total < self.blue.total):
            self.winner = "blue"
        else:
            self.winner = "tie"

    def print(self):
        print("Red: ", self.red.str())
        print("Blue:",self.blue.str())
        print("Winner - ",self.winner)
        print("Red Score: ",self.red.total)
        print("Blue Score: ",self.blue.total)
        print("\n")

class schedule:
    def __init__(self,teamSet={}) -> None:
        self.teamSet = teamSet
        self.matches = []

    def gen_matches(self, n):
        #will deal with surrogates later
        #could be more nuanced, but this should work
        while(n>0):
            teamList = list(self.teamSet)
            random.shuffle(teamList)
            while(len(teamList) >= 6):
                red = alliance([teamList.pop(0),teamList.pop(0),teamList.pop(0)])
                blue = alliance([teamList.pop(0),teamList.pop(0),teamList.pop(0)])
                self.matches.append(match(red,blue))
                n = n-1

class event:
    def __init__(self,attrGen,nTeams = 0,nMatches = 0) -> None:
        self.teamSet = set()
        for x in range(0,nTeams):
            self.teamSet.add(teamReal(1000+x,attrGen))
        self.schedule = schedule(self.teamSet)
        self.schedule.gen_matches(nMatches)

    def play(self,scorer):
        for m in self.schedule.matches:
            m.play(scorer)
    
    def printMatchResults(self):
        for m in self.schedule.matches:
            m.print()
    def printTopRanked(self,nTop,ranker):
        ranks = ranker(self.schedule.matches)
        for i in min(len(ranks),nTop):
            print("Rank ",i,":",ranks[i].number)
            print(ranks[i].attrBounds)
#gah need to write a quick ranker
