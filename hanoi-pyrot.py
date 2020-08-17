#!/usr/bin/env python3

class HanoiRotation:
    def __init__(self, n_pools, tapes_per_pool):
        self.__n_pools = n_pools
        self.__tapes_per_pool = tapes_per_pool
        # Stack will contain (verb, pool) couples
        # * verb is 'e' (execute) or 'v' (value) - yes not a real verb
        # * pool is a pool id
        self.__stack = []
        self.__tapes = [0] * self.__n_pools

    def __next_pool(self):
        while True:
            if len(self.__stack) == 0:
                self.__stack.append(['e', self.__n_pools-1])
                return self.__n_pools-1

            verb, pool = self.__stack.pop()
            
            if verb == 'e':
                if pool == 0:
                    self.__stack.append(['v', 0])
                    
                else:
                    self.__stack.append(['e', pool-1])
                    self.__stack.append(['v', pool])
                    self.__stack.append(['e', pool-1])
                
            elif verb == 'v':
                return pool

            else:
                raise ValueError("Unknown verb: '{}'".format(verb))
            
    def __next_pool_tape(self, pool_id):
        tape = self.__tapes[pool_id]
        self.__tapes[pool_id] = (self.__tapes[pool_id] + 1) % self.__tapes_per_pool
        return tape
        
    def next_tape(self):
        """
        Returns a couple (pool_id, pool_tape_id)
        """
        pool = self.__next_pool()
        tape = self.__next_pool_tape(pool)
        return (pool, tape)


def test_4pools_1tape():
    expected = [(3,0), (0,0), (1,0), (0,0), (2,0), (0,0), (1,0), (0,0),
                (3,0), (0,0), (1,0), (0,0), (2,0), (0,0), (1,0), (0,0),
                (3,0), (0,0), (1,0), (0,0), (2,0), (0,0), (1,0), (0,0)]
    hanoi = HanoiRotation(4, 1)
    for i, v in enumerate(expected):
        t = hanoi.next_tape()
        print(t)
        if v != t:
            print("*Error* at iteration {}: expected tape '{}' but got '{}'".format(i, v, t))
    
def test_4pools_2tapes():
    expected = [(3,0), (0,0), (1,0), (0,1), (2,0), (0,0), (1,1), (0,1),
                (3,1), (0,0), (1,0), (0,1), (2,1), (0,0), (1,1), (0,1),
                (3,0), (0,0), (1,0), (0,1), (2,0), (0,0), (1,1), (0,1)]
    hanoi = HanoiRotation(4, 2)
    for i, v in enumerate(expected):
        t = hanoi.next_tape()
        print(t)
        if v != t:
            print("*Error* at iteration {}: expected tape '{}' but got '{}'".format(i, v, t))

def test():
    print("test_4pools_1tape")
    test_4pools_1tape()
    print("test_4pools_2tapes")
    test_4pools_2tapes()

def main():
    hanoi = HanoiRotation(20, 2)
    for i in range(365):
        print(i, hanoi.next_tape())


main()
