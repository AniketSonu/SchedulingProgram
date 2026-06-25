
class Course:

    def __init__(
            self,
            cid,
            students,
            professor,
            professor_availability,
            professor_preferences=None):

        self.id = cid
        self.students = students
        self.professor = professor

        self.professor_availability = (
            professor_availability
        )

        self.professor_preferences = (
            professor_preferences or {}
        )

class Room:

    def __init__(self,
                 rid,
                 capacity,
                 availability,
                 restricted_slots=None):

        self.id = rid
        self.capacity = capacity
        self.availability = availability
        self.restricted_slots = (
            restricted_slots or {}
        )