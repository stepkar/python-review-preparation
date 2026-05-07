class Solution(object):
  def gcdOfStrings(self, str1, str2):
    """
    :type str1: str
    :type str2: str
    :rtype: str
    """
    for char1, char2 in zip(str1, str2):
      if char1 != char2:
        return ""

    if len(str1) == len(str2):
      return str1
    if set(str1) != set(str2):
      return ""
    if str1+str2 != str2 + str1:
      return ""

    def gcd(a, b):
      while b:
        a, b = b, a % b
      return a
    g = gcd(len(str1), len(str2))
    return str1[:g]








if __name__ == '__main__':
    s = Solution()

    print(s.gcdOfStrings("ABCABC", "ABC"))
    print(s.gcdOfStrings("ABABAB", "ABAB"))
    print(s.gcdOfStrings("LEET", "CODE"))
    print(s.gcdOfStrings("AAAAAB", "AAA"))