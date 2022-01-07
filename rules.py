#some fp stuff
def mult(a):
    def y(x):
        return a*x
    return y

infRechargeSimple = {
    "innerGoals":mult(3),
    "outerGoals":mult(2)
}