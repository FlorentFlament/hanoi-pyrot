#!/usr/bin/env python3
import json # to store and load state

DEFAULT_STATE_FILENAME="hanoi_pyrot.state"

class HanoiRotation:
    def from_scratch(n_pools, tapes_per_pool):
        hanoi = HanoiRotation()
        hanoi.__n_pools = n_pools
        hanoi.__tapes_per_pool = tapes_per_pool
        # Stack will contain (verb, pool) couples
        # * verb is 'e' (execute) or 'v' (value) - yes not a real verb
        # * pool is a pool id
        hanoi.__stack = []
        hanoi.__tapes = [0] * n_pools
        return hanoi

    def from_statefile(fname=DEFAULT_STATE_FILENAME):
        hanoi = HanoiRotation()
        hanoi.__load_state(fname)
        return hanoi

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

    def __next_tape(self, pool_id):
        tape = self.__tapes[pool_id]
        self.__tapes[pool_id] = (self.__tapes[pool_id] + 1) % self.__tapes_per_pool
        return tape

    def next(self):
        """
        Returns a couple (pool_id, pool_tape_id)
        """
        pool = self.__next_pool()
        tape = self.__next_tape(pool)
        return (pool, tape)

    def __load_state(self, fname=DEFAULT_STATE_FILENAME):
        with open(fname, 'r') as fd:
            for k,v in json.load(fd).items():
                setattr(self, k, v)

    def save_state(self, fname=DEFAULT_STATE_FILENAME):
        with open(fname, 'w') as fd:
            json.dump(self.__dict__, fd, sort_keys=True)


def test_4pools_1tape():
    expected = [(3,0), (0,0), (1,0), (0,0), (2,0), (0,0), (1,0), (0,0),
                (3,0), (0,0), (1,0), (0,0), (2,0), (0,0), (1,0), (0,0),
                (3,0), (0,0), (1,0), (0,0), (2,0), (0,0), (1,0), (0,0)]
    hanoi = HanoiRotation.from_scratch(4, 1)
    for i, v in enumerate(expected):
        t = hanoi.next()
        if v != t:
            print("*Error* at iteration {}: expected tape '{}' but got '{}'".format(i, v, t))

def test_4pools_2tapes():
    expected = [(3,0), (0,0), (1,0), (0,1), (2,0), (0,0), (1,1), (0,1),
                (3,1), (0,0), (1,0), (0,1), (2,1), (0,0), (1,1), (0,1),
                (3,0), (0,0), (1,0), (0,1), (2,0), (0,0), (1,1), (0,1)]
    hanoi = HanoiRotation.from_scratch(4, 2)
    for i, v in enumerate(expected):
        t = hanoi.next()
        if v != t:
            print("*Error* at iteration {}: expected tape '{}' but got '{}'".format(i, v, t))

def test():
    print("test_4pools_1tape")
    test_4pools_1tape()
    print("test_4pools_2tapes")
    test_4pools_2tapes()
    print("done")

def distribution():
    backups = {}
    # Favorite setup: 15 pools, 2 tapes per pool -> 30 tapes
    # Oscillates between 67 and 89 years of backup - 1.5 * 2**(15-1) / 365
    hanoi = HanoiRotation.from_scratch(15, 2)
    for i in range(365*50):
        backups[hanoi.next()]= i
        v = sorted(backups.values())
        print(i, round((v[-1]-v[0])/365, 2), [a-b for a,b in zip(v[1:], v[:-1])])
    print(v)

def main():
    try:
        hanoi = HanoiRotation.from_statefile()
    except FileNotFoundError:
        hanoi = HanoiRotation.from_scratch(15, 2)
    pool, tape = hanoi.next()
    print("{}-{}".format(pool, tape))
    hanoi.save_state()

main()
