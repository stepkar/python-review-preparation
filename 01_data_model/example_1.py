import collections
import math

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
  rank = [str(n) for n in range(2, 11)] + list('ВДКТ')
  suit = 'черви бубна пики крести'.split()

  def __init__(self):
    self._cards = [Card(rank, suit) for suit in self.suit
                 for rank in self.rank]

  def __len__(self):
    return len(self._cards)

  # Чтобы можно было получать доступ через my_collection[key]
  def __getitem__(self, item):
    return self._cards[item]

def spades_high(card):
  rank_value = FrenchDeck.rank.index(card.rank)
  return rank_value * len(suit_values) + suit_values[card.suit]

suit_values=dict(черви=3, крести = 2, пики=1, бубна = 0)

if __name__ in '__main__':

  test_dic = {}
  test_dic['some'] = 4
  print(test_dic['some'])


  fd = FrenchDeck()
  print('***********************************')
  print(fd[:3])
  print(fd[12::13])
  print(Card('Т', 'черви') in fd)
  index = fd._cards.index(Card('Т', 'черви'))
  print(index)




