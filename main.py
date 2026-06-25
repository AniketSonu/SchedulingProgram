import math
from models import Course
from parser import load_data
from greedy_solver import GreedySolver
from graph_engine import GraphEngine

def main():

    courses, rooms, groups, timeslots = load_data()

    max_room_capacity = max(
        room.capacity for room in rooms
    )

    expanded_courses = []

    for course in courses:


        if course.students <= max_room_capacity:
            expanded_courses.append(course)

        # Split large classes
        else:

            num_groups = math.ceil(
                course.students / max_room_capacity
            )

            students_per_group = math.ceil(
                course.students / num_groups
            )

            print(
                f"{course.id} split into "
                f"{num_groups} sections"
            )

            for i in range(num_groups):
                new_course = Course(
                    cid=f"{course.id}_{chr(65 + i)}",
                    students=students_per_group,
                    professor=course.professor,
                    professor_availability=
                    course.professor_availability,
                    professor_preferences=
                    course.professor_preferences
                )

                expanded_courses.append(new_course)

    # Replace original course list
    courses = expanded_courses
    updated_groups = {}

    for group_name, class_ids in groups.items():

        new_class_ids = []

        for cid in class_ids:

            split_sections = [
                course.id
                for course in courses
                if course.id.startswith(cid + "_")
            ]

            if split_sections:
                new_class_ids.extend(split_sections)
            else:
                new_class_ids.append(cid)

        updated_groups[group_name] = new_class_ids

    groups = updated_groups
    course_map = {
        course.id: course
        for course in courses
    }

    print("\n--- Schedule Room Table ---\n")

    greedy = GreedySolver()

    schedule = greedy.solve(
        courses,
        rooms,
        timeslots,
        groups
    )


    graph_engine = GraphEngine()

    graph, conflicts = graph_engine.build_graph(
        courses,
        groups
    )

    for cid, result in schedule.items():

        professor = course_map[cid].professor

        if result:

            slot, room = result

            print(
                f"Scheduled {cid}"
                f" | Professor: {professor}"
                f" | {slot}"
                f" | Room {room}"
            )

        else:

            print(
                f"Unscheduled {cid}"
                f" | Professor: {professor}"
            )

    print("\n--- Group Divided and time slot ---\n")


    colors = graph_engine.welsh_powell(graph)

    for cls, color in colors.items():
        print(
            f"{cls} -> Time Slot Group {color}"
        )

    print("\n--- CONFLICT Report ---\n")

    for conflict in conflicts:
        print(
            f"{conflict['type']}: "
            f"{conflict['class1']} <-> {conflict['class2']} "
            f"({conflict['reason']})"
        )


if __name__ == "__main__":
    main()