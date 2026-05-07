
class Solution(object):
  def mergeAlternately(self, word1, word2):
    """
    :type word1: str
    :type word2: str
    :rtype: str
    """
    import itertools
    return ''.join(a + b for a, b in itertools.zip_longest(word1,word2, fillvalue=''))

if __name__=="__main__":
  # longest = itertools.zip_longest('ABCD', 'xy', fillvalue='')
  # for i in longest:
  #   print(i)

  s = Solution()
  print(s.mergeAlternately('123456', '123'))