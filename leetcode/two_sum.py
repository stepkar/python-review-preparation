class Solution(object):
  def twoSum(self, nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    if len(nums) == 2:
      return [0, 1]

    temp_idx = 0
    length = len(nums) - 1
    while temp_idx != length:
      for idx, value in enumerate(nums[temp_idx+1:]):
        if value + nums[temp_idx] == target:
          return [temp_idx, temp_idx+idx+1]
      temp_idx = temp_idx + 1

if __name__ == "__main__":
  s = Solution()

  nums = [15,2,26,7]
  target = 9
  print(s.twoSum(nums, target))