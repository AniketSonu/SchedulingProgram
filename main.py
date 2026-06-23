from parser import load_data
from greedy_solver import GreedySolver
from graph_engine import GraphEngine

def main():

    courses, rooms, groups, timeslots = load_data()

    print("\n--- GREEDY SCHEDULE ---\n")

    greedy = GreedySolver()

    schedule = greedy.solve(
        courses,
        rooms,
        timeslots,
        groups
    )

    # Create GraphEngine first
    graph_engine = GraphEngine()

    graph, conflicts = graph_engine.build_graph(
        courses,
        groups
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

            print(f"Unscheduled {cid}")

    print("\n--- GRAPH COLORING ---\n")

    # No need to build the graph again
    colors = graph_engine.welsh_powell(graph)

    for cls, color in colors.items():
        print(
            f"{cls} -> Time Slot Group {color}"
        )

    print("\n--- CONFLICT REPORT ---\n")

    for conflict in conflicts:
        print(
            f"{conflict['type']}: "
            f"{conflict['class1']} <-> {conflict['class2']} "
            f"({conflict['reason']})"
        )


if __name__ == "__main__":
    main()