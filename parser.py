import json
from models import Course, Room


def load_data():

    with open("data/classdata.json") as f:
        data = json.load(f)

    professor_map = {}

    for prof in data["professors"]:
        professor_map[prof["id"]] = (
            prof["availability"]
        )


    courses = []

    for c in data["classes"]:
        courses.append(

            Course(
                cid=c["id"],
                students=c["students"],
                professor=c["professor"],
                professor_availability=
                professor_map.get(
                    c["professor"], {}
                )
            )
        )

    rooms = []

    for r in data["rooms"]:
        rooms.append(

            Room(
                rid=r["id"],
                capacity=r["capacity"],
                availability=r["availability"],
                restricted_slots=
                r.get(
                    "restricted_slots", {}
                )
            )
        )

    student_groups = data["student_groups"]

    timeslots = data["timeslots"]

    return (
        courses,
        rooms,
        student_groups,
        timeslots
    )