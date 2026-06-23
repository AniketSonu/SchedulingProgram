class GreedySolver:



    def room_available(self, room, slot):

        day, hour = slot.split("-")

        # Room available on that day?
        if not room.availability.get(day, False):
            return False

        # Check restricted slots (MacPool etc.)
        if hasattr(room, "restricted_slots"):

            if day in room.restricted_slots:

                if hour in room.restricted_slots[day]:
                    return False

        return True


    def solve(
            self,
            courses,
            rooms,
            timeslots,
            student_groups):

        schedule = {}

        room_occupied = set()
        professor_occupied = set()
        group_occupied = set()


        professor_daily_load = {}



        course_to_group = {}

        for group, cls_list in student_groups.items():

            for cls in cls_list:
                course_to_group[cls] = group



        courses = sorted(
            courses,
            key=lambda x: x.students,
            reverse=True
        )

        slot_index = 0


        for course in courses:

            placed = False

            # Rotate slots to spread classes
            for i in range(len(timeslots)):

                slot = timeslots[
                    (slot_index + i)
                    % len(timeslots)
                ]

                day, hour = slot.split("-")

                if not course.professor_availability.get(
                        day,
                        True):
                    continue

                prefs = getattr(
                    course,
                    "professor_preferences",
                    {}
                )

                preferred_days = prefs.get(
                    "preferred_days",
                    []
                )

                if (
                        preferred_days and
                        day not in preferred_days
                ):
                    continue

                preferred_times = prefs.get(
                    "preferred_times",
                    []
                )

                if (
                        preferred_times and
                        hour not in preferred_times
                ):
                    continue

                current_load = professor_daily_load.get(
                    (course.professor, day),
                    0
                )

                max_load = prefs.get(
                    "max_classes_per_day",
                    99
                )

                if current_load >= max_load:
                    continue

                if (
                        slot,
                        course.professor
                ) in professor_occupied:
                    continue

                group = course_to_group.get(
                    course.id
                )

                if group and (
                        slot,
                        group
                ) in group_occupied:
                    continue

                available_rooms = sorted(
                    rooms,
                    key=lambda r:
                    r.capacity - course.students
                    if r.capacity >= course.students
                    else 9999
                )

                for room in available_rooms:

                    if room.capacity < course.students:
                        continue

                    if not self.room_available(
                            room,
                            slot):
                        continue

                    # Room already occupied?

                    if (
                            slot,
                            room.id
                    ) in room_occupied:
                        continue

                    schedule[course.id] = (
                        slot,
                        room.id
                    )

                    room_occupied.add(
                        (slot, room.id)
                    )

                    professor_occupied.add(
                        (
                            slot,
                            course.professor
                        )
                    )

                    if group:
                        group_occupied.add(
                            (slot, group)
                        )

                    professor_daily_load[
                        (
                            course.professor,
                            day
                        )
                    ] = current_load + 1

                    placed = True

                    slot_index += 1

                    break

                if placed:
                    break

            if not placed:
                schedule[course.id] = None

        return schedule