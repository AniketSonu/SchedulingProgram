class Backtracker:

    def __init__(self):

        self.best = {}
        self.best_unscheduled = 999

    def search(self,
               idx,
               courses,
               schedule):

        if idx == len(courses):

            unscheduled = sum(
                1 for v in schedule.values()
                if v is None
            )

            if unscheduled < self.best_unscheduled:

                self.best_unscheduled = unscheduled
                self.best = schedule.copy()

            return

        course = courses[idx]

        schedule[course.id] = None

        self.search(
            idx + 1,
            courses,
            schedule
        )