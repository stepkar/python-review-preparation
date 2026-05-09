class Solution(object):
  def reverseWords(self, s):
    """
    :type s: str
    :rtype: str
    """
    return ' '.join(reversed(list(filter(None,s.split(' ')))))


if __name__ == '__main__':

    s = Solution()
    print(s.reverseWords("a good   example"))