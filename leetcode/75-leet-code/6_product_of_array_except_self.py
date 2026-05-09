from functools import reduce

from setuptools.command.install_egg_info import install_egg_info


class Solution(object):
  def productExceptSelf(self, nums):
    """
    :type nums: List[int]
    :rtype: List[int]
    """
# решение не прошло по времени. Копирование массива O^n итого О^n^2 и reduce O^n итого О^n^2 + О^n^2
    # answer=[0]*len(nums)
    # for i, num in enumerate(nums):
    #   temp = list(nums)
    #   # del temp[i]
    #   temp.pop(i)
    #   product = reduce(lambda acc, x: acc * x, temp)
    #   answer[i] = product

    '''
    гипотеза: сделать заранее два массива с перемножением левой и правой части от i-ого
    элемента в nums
    Да, будет n*3 но это всё равно O(n)
    пример
    
    [3, 2, 1, 0, 4, 5]
   должен получиться массив:
    [0,0,0,120,0,0]
   
   l[1, 3, 6, 6, 0, 0]
   r[0, 0, 0, 20,5, 1]
   допустим мы на четвёртой позиции. Слева 3*2*1=6, справа 4*5=20 => 6*20=120
    '''


    length = len(nums)
    l,r = [1]*length, [1]*length
    answer=[0]*length
    for i in range(length-2, -1, -1):
      r[i]=r[i+1]*nums[i+1]

    for i in range(1,length):
      l[i] = l[i-1] * nums[i-1]

    for i in range(length):
      answer[i]=l[i]*r[i]
    print(answer)
    return answer



if __name__ == '__main__':
  s = Solution()
  s.productExceptSelf([3, 2, 1, 0, 4, 5])