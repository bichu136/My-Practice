class state():
    def __init__(self,thieves = 3,billionare= 3,boat = True):
        self.thieves = thieves
        self.billionare= billionare
        self.boat = boat
        self.visitted = False
        self.fr = None
    def __eq__(self, other):
        return self.thieves == other.thieves and self.billionare== other.billionare and self.boat ==  other.boat
    def __str__(self):
        return "billionare:{}\n thieves: {}\n boat: {}\n".format(self.billionare,self.thieves,self.getBoat())
    def getBoat(self):
        if self.boat:
            return "boat is on this side"
        else:
            return "boat is on the other side"
    def  getNextState(self):
        r = []
        if self.boat:
            if self.thieves >0 and self.billionare>0:
                r.append(state(thieves=self.thieves -1,billionare= self.billionare-1,boat = False))
            if self.thieves >= 2:
                r.append(state(thieves = self.thieves -2, billionare= self.billionare,boat = False))
            if self.billionare>=2:
                r.append(state(thieves = self.thieves, billionare= self.billionare-2,boat = False))
            if self.billionare>=1:
                r.append(state(thieves = self.thieves, billionare= self.billionare-1,boat = False))
            if self.thieves>=1:
                r.append(state(thieves = self.thieves-1, billionare= self.billionare,boat = False))
        else:
            if self.thieves <3 and self.billionare<3:
                r.append(state(thieves=self.thieves +1,billionare= self.billionare+1))
            if self.thieves <3:
                r.append(state(thieves = self.thieves +1, billionare= self.billionare))
            if self.billionare<=1:
                r.append(state(thieves = self.thieves, billionare= self.billionare+2))
            if self.billionare<3:
                r.append(state(thieves = self.thieves, billionare= self.billionare+1))
            if self.thieves<=1:
                r.append(state(thieves = self.thieves+2, billionare= self.billionare))
        return r
    def is_dead(self):
        other_billionares = 3-self.billionare
        other_thieves = 3 - self.thieves
        if other_billionares != 0 and other_thieves !=0:
            if other_billionares< other_thieves:
                return True
        if self.billionare!= 0 and self.thieves !=0:
            if self.billionare<self.thieves:
                return True
        return False

# các state:
#     số cừu còn ở lại:<=3 số sói còn ở lại<=3
# các loại bước đi:
# nếu thuyền bên kia:
#         nếu số sói <3 và số cừu <3:
#         +1 sói +1 cừu
#         nếu số sói <3:
#         +1 sói
#         nếu số sói <2:
#         +2 sói
#         nếu số cừu <=1:
#         +2 cừu
#         nếu số cừu<3:
#         +1 cừu
# nếu thuyền bên đây:
#         nếu số sói>0 và số cừu>0:
#         -1 sói -1 cừu
#         nếu số sói>=2:
#         -2 sói
#         nếu số sói>=1:
#         -1 sói
#         nếu số cừu >=2:
#         -2 cừu
#         nếu số sói >=1:
#         -1 cừu
# deadstate:
# số cừu > số sói hoặc số sói > số cừu
# goal state:ass state(:
# số cừu = 0 và số sói = 0
open = []

close = []

thieves = 3
billionare= 3
c = state(thieves = thieves,billionare= billionare)

open.append(c)

while open !=[]:
    c = open[0]
    if c.billionare==0 and c.thieves == 0:
        break
    next = c.getNextState()
    for st in next:
        if not st.is_dead():

            # check if in close or not
            b =True
            for tst in close:
                if st == tst:
                    b = False
                    break
            if b:
                st.fr = c
                open.append(st)

    close.append(c)
    open.remove(c)
path = []
while c is not None:
    path.append(c)
    c = c.fr
path.reverse()

for o in path:
    print(o)

