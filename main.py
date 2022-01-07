from sim import teamStatic,teamReal,alliance,match,schedule
from sim import boundGen as bg
from rules import basicScorer
import rules

#a demo of what these scripts can do
#can be quickly changed by writing new rulesets in rules.py


#with static teams( most explicit, but very verbose)
IRsimple = basicScorer(rules.infRechargeSimple)

print("\nStatic 1-Match Example:\n")
r1 = teamStatic(1001,{
    "innerGoals":3,
    "outerGoals":6,
    "climbs":1
})

r2 = teamStatic(2001,{
    "innerGoals":1,
    "outerGoals":2,
    "climbs":2
})

#can omit fields that have no value
r3 = teamStatic(3001,{
    "innerGoals":5
})

b1 = teamStatic(4001,{
    "outerGoals":3,
    "climbs":1
})

b2 = teamStatic(5001,{
    "climbs":2
})

b3 = teamStatic(6001,{
    "outerGoals":7
})


m = match(alliance([r1,r2,r3]),alliance([b1,b2,b3]))
m.play(IRsimple)
m.print()
print("\n")

#can grab more info if you want it
print("Red alliance objects scored:")
print(m.red.comboResult,"\n")

print("Blue Team 1:",m.blue.teams[0].number," attributes:")
print(m.blue.teams[0].attr,"\n")

print("\n")

#using teamReal and boundGenerators,much more can be done
