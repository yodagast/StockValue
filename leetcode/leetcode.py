class Solution:
    def findRadius(self, houses, heaters):
        heaters=sorted(heaters)+[float('inf')]
        i,maxRadius=0,0
        for h in sorted(houses):
            while(i+1<len(heaters) & heaters[i]+heaters[i+1]<=2*h):
                i=i+1
            maxRadius=max(maxRadius,abs(heaters[i]-h))
        return maxRadius

    def arrangeCoins(self, n: int):
        cnt,i=0,1
        while(cnt<n):
            cnt=cnt+1
            i+=1
        return i-1;

    def findDisappearedNumbers(self, nums):

