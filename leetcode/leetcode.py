class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
class Solution1:
    def countNodes(self, root: TreeNode) -> int:
        if(root.val!=None):
            return 1+countNodes(root.left)+countNodes(root.right)
class Solution:
    def findRadius(self, houses, heaters):
        heaters=sorted(heaters)+[float('inf')]
        i,maxRadius=0,0
        for h in sorted(houses):
            while(i+1<len(heaters) & heaters[i]+heaters[i+1]<=2*h):
                i=i+1
            maxRadius=max(maxRadius,abs(heaters[i]-h))
        return maxRadius

    def arrangeCoins(self, n):
        cnt,i=0,1
        while(cnt<n):
            cnt=cnt+1
            i+=1
        return i-1;

    def maxProfit(self, k, prices) -> int:
        dp=[[ 0 for i in range(prices)] for j in range(k+1)]
        res=0
        n=len(prices)
        for i in range(1,k):
            tmp=dp[i][0]-prices[0]
            for j in range(1,n):
                dp[i][j]=max(dp[i][j-1],tmp+prices[j])
                tmp=max(tmp,dp[i-1][j]+prices[j])
                res=max(res,dp[i][j])
        return res



    def isIsomorphic(self, s: str, t: str):
        return [s.find(i) for i in s]==[t.find(i) for i in t]





