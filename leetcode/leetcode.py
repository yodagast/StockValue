class Solution:
    def findRadius(self, houses, heaters):
        houses.sort()
        heaters.sort()
        i,maxRadius=0,0
        for h in houses:
            while(i+1<len(heaters) & heaters[i]+heaters[i+1]<=2*h):
                i=i+1
            maxRadius=max(maxRadius,abs(heaters[i]-h))
        return maxRadius

