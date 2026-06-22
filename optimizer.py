from functools import lru_cache


class Optimizer:

    def assign_rooms(self, classes, rooms):

        n = len(classes)

        @lru_cache(None)
        def dp(i, mask):

            if i == n:
                return (0, [])

            cls = classes[i]

            best_cost = float('inf')
            best_assignment = []

            for r in range(len(rooms)):

                if mask & (1 << r):
                    continue

                room = rooms[r]

                if room.capacity < cls.students:
                    continue

                waste = room.capacity - cls.students

                cost, assign = dp(
                    i + 1,
                    mask | (1 << r)
                )

                total = waste + cost

                if total < best_cost:

                    best_cost = total
                    best_assignment = \
                        [(cls.id, room.id)] + assign

            return best_cost, best_assignment

        return dp(0, 0)