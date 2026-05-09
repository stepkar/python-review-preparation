from collections import deque


class Solution(object):
  def reverseVowels(self, s):
    """
    :type s: str
    :rtype: str
    """
    vowels = {'a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y'}
    arr = ['']*len(s)
    left, right = 0, len(s) - 1
    while left <= right:
      if s[left] in vowels and s[right] in vowels:
        arr[left],arr[right] = s[right], s[left]
        right += -1
        left += 1
      elif s[left] in vowels and s[right] not in vowels:
        arr[right] = s[right]
        right += -1
      elif s[right] in vowels and s[left] not in vowels:
        arr[left]=s[left]
        left += 1
      else:
        arr[left],arr[right]=s[left],s[right]
        right += -1
        left += 1
    return ''.join(arr)


if __name__ == '__main__':
  test = 'Yo! Bottoms up, U.S. Motto, boy!'
  s = Solution()
  print(s.reverseVowels(test))
