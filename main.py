from parser import load_data
from greedy_solver import GreedySolver
from graph_engine import GraphEngine
from optimizer import Optimizer


def main():

    courses, rooms, groups, timeslots = load_data()

    print("\n--- GREEDY SCHEDULE ---\n")

    greedy = GreedySolver()

    schedule = greedy.solve(
        courses,
        rooms,
        timeslots
    )

    for cid, result in schedule.items():

        if result:

            slot, room = result

            print(
                f"Scheduled {cid}"
                f" | {slot}"
                f" | Room {room}"
            )

        else:

            print(
                f"Unscheduled {cid}"
            )

    print("\n--- GRAPH COLORING ---\n")

    graph_engine = GraphEngine()

    graph, conflicts = graph_engine.build_graph(
        courses,
        groups
    )

    colors = graph_engine.welsh_powell(graph)

    for cls, color in colors.items():
        print(
            f"{cls} -> Time Slot Group {color}"
        )

    print("\n--- DP ROOM OPTIMIZATION ---\n")

    optimizer = Optimizer()

    cost, allocation = optimizer.assign_rooms(
        courses,
        rooms
    )

    print("Total wasted seats:", cost)

    for c, r in allocation:
        print(c, "->", r)


if __name__ == "__main__":
    main()