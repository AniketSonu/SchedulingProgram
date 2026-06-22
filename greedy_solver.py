class GreedySolver:

    def room_available(self, room, slot):

        day, hour = slot.split("-")

        if not room.availability[day]:
            return False

        if day in room.restricted_slots:
            if hour in room.restricted_slots[day]:
                return False

        return True

    def solve(self, courses, rooms, timeslots):

        schedule = {}
        occupied = set()

        courses = sorted(
            courses,
            key=lambda x: x.students,
            reverse=True
        )

        for course in courses:

            placed = False

            for slot in timeslots:

                for room in rooms:

                    if room.capacity < course.students:
                        continue

                    if not self.room_available(room, slot):
                        continue

                    if (slot, room.id) in occupied:
                        continue

                    schedule[course.id] = (
                        slot,
                        room.id
                    )

                    occupied.add((slot, room.id))

                    placed = True
                    break

                if placed:
                    break

            if not placed:
                schedule[course.id] = None

        return schedule