class Course:
    def __init__(self, cid, students, professor):
        self.id = cid
        self.students = students
        self.professor = professor


class Room:
    def __init__(self, rid, capacity, availability,
                 restricted_slots=None):

        self.id = rid
        self.capacity = capacity
        self.availability = availability
        self.restricted_slots = restricted_slots or {}