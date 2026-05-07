from typing import List


class Solution:
  def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
    rule=3
    neibour=True
    for i in flowerbed:
      if i == 0:
        if rule >0:
          if neibour:
            rule=rule-1
            neibour=False
          rule=rule-1
        if rule==0:
          n=n-1
          neibour=True
          rule=3
      if i==1:
        rule=3
        neibour=False
    if rule==1:
      if n >0:
        n=n-1

    if n<0:
      n=0
    print(n==0)
    return n == 0

if __name__ == '__main__':
    s=Solution()
    s.canPlaceFlowers([0,0,0,0], 1)