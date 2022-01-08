from sim import teamStatic,teamReal,alliance,match,schedule,event
from sim import boundGen as bg
from rules import basicScorer
import rules

RRscorer = basicScorer(rules.RR)

simplebg = {
    "taxi":bg(0,0,1,1),
    "autoLower":bg(0,2,2,4),
    "autoUpper":bg(0,1,2,4),
    "teleopLower":bg(0,5,6,10),
    "teleopUpper":bg(0,5,6,8),
    "climbs": bg(0,2,2,4)
}

test_event = event(simplebg,100,6000)
test_event.play(RRscorer)
test_event.printTopRanked(10,rules.RR_ranker)