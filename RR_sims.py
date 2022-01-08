from sim import teamStatic,teamReal,alliance,match,schedule,event
from sim import boundGen as bg
from rules import basicScorer
import rules

RRscorer = basicScorer(rules.RR)

#let's ignore auto lower for noe, since I have no bound on connected things
simplebg = {
    "taxi":bg(0,0,1,1),
    "autoLower":bg(0,0,0,1),
    "autoUpper":bg(0,1,2,5),
    "teleopLower":bg(5,5,6,15),
    "teleopUpper":bg(5,5,6,15),
    "climbs": bg(0,2,2,5)
}

test_event = event(simplebg,500,12000)
test_event.play(RRscorer)
test_event.printTopRanked(10,rules.RR_ranker)