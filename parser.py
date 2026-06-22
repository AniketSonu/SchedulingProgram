import json
from models import Course, Room


def load_data():

    with open("data/classdata.json") as f:
        data = json.load(f)

    courses = []

    for c in data["classes"]:
        courses.append(
            Course(
                c["id"],
                c["students"],
                c["professor"]
            )
        )

    rooms = []

    for r in data["rooms"]:

        rooms.append(
            Room(
                r["id"],
                r["capacity"],
                r["availability"],
                r.get("restricted_slots", {})
            )
        )

    return (
        courses,
        rooms,
        data["student_groups"],
        data["timeslots"]
    )