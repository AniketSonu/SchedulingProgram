class GreedySolver:

    def room_available(self, room, slot):

        day, hour = slot.split("-")

        if not room.availability[day]:
            return False

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

            # Rotate starting slot
            for i in range(len(timeslots)):

                slot = timeslots[
                    (slot_index + i)
                    % len(timeslots)
                    ]

                day, _ = slot.split("-")

                if not course.professor_availability.get(
                        day,
                        True):
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
                )

                for room in available_rooms:

                    if room.capacity < course.students:
                        continue

                    if not self.room_available(
                            room,
                            slot):
                        continue



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

                    placed = True

                    slot_index += 1

                    break

                if placed:
                    break

            if not placed:
                schedule[course.id] = None

        return schedule