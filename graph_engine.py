from collections import defaultdict


class GraphEngine:

    def build_graph(self, courses, student_groups):

        graph = defaultdict(set)
        conflict_report = []


        for group, class_list in student_groups.items():

            for i in range(len(class_list)):
                for j in range(i + 1, len(class_list)):

                    c1 = class_list[i]
                    c2 = class_list[j]

                    graph[c1].add(c2)
                    graph[c2].add(c1)

                    conflict_report.append(
                        {
                            "type": "Student Group Conflict",
                            "class1": c1,
                            "class2": c2,
                            "reason": f"Both belong to {group}"
                        }
                    )


        professor_map = defaultdict(list)

        for course in courses:
            professor_map[course.professor].append(course.id)

        for professor, class_list in professor_map.items():

            if len(class_list) > 1:

                for i in range(len(class_list)):
                    for j in range(i + 1, len(class_list)):

                        c1 = class_list[i]
                        c2 = class_list[j]

                        graph[c1].add(c2)
                        graph[c2].add(c1)

                        conflict_report.append(
                            {
                                "type": "Professor Conflict",
                                "class1": c1,
                                "class2": c2,
                                "reason": f"Same Professor ({professor})"
                            }
                        )

        return graph, conflict_report



    def welsh_powell(self, graph):

        ordering = sorted(
            graph.keys(),
            key=lambda x: len(graph[x]),
            reverse=True
        )

        colors = {}
        current_color = 0

        for node in ordering:

            if node in colors:
                continue

            colors[node] = current_color

            for other in ordering:

                if other in colors:
                    continue

                can_color = True

                for neighbor in graph[other]:
                    if colors.get(neighbor) == current_color:
                        can_color = False
                        break

                if can_color:
                    colors[other] = current_color

            current_color += 1

        return colors