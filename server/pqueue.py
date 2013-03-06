"""
Priority queue implemented with dictionaries.  Stores a set of keys
and associated priorities.

pop_smallest()
  Removes the key with the smallest priority and return a tuple
  with the key and priority.

update(key, priority)
  If priority is lower than the associated priority of key, then
  change key's priority.  If not, does nothing.

  If key is not in the priority queue, add it.

  Returns nothing.

is_empty()
  Returns True if empty, else False

>>> q = PQueue()
>>> q.is_empty()
True
>>> q.update("thing", 5)
>>> q.is_empty()
False
>>> q.update("another thing", 2)
>>> q.pop_smallest()
('another thing', 2)
>>> q.update("thing", 100)
>>> q.update("something else", 110)
>>> q.update("something else", 8)
>>> q.pop_smallest()
('thing', 5)
>>> q.pop_smallest()
('something else', 8)
>>> q.is_empty()
True

"""

class PQueue:
    def __init__(self):
        self._q = {}

    def pop_smallest(self):
        k = min(self._q, key=self._q.get)
        p = self._q.pop(k)
        return (k, p)

    def update(self, key, priority):
        if key not in self._q or self._q[key] > priority:
            self._q[key] = priority

    def is_empty(self):
        if self._q:
            return False
        else:
            return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
