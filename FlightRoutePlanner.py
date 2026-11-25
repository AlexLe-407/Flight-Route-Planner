import networkx as nx
import matplotlib.pyplot as plt

flights = {
    "MCI": {"DFW": 460, "DEN": 533, "ORD": 403, "ATL": 692, "BWI": 963},
    "DFW": {"ORD": 802, "ATL": 731, "LAX": 1232, "IAH": 224 },
    "DEN": {"MCI": 533, "LAX": 862, "ORD": 888, "SLC": 391},
    "ORD": {"DFW": 802, "JFK": 740, "ATL": 606, "BOS": 867},
    "ATL": {"MCI": 692, "ORD": 606, "MIA": 594, "CLT": 226},
    "LAX": {"DEN": 862, "JFK": 2470, "SFO": 337, "SEA": 954},
    "JFK": {"ATL": 760, "ORD": 740, "BOS": 187, "MIA": 1090},
    "SEA": {"LAX": 954, "SFO": 679, "DEN": 1024, "PDX": 129},
    "SFO": {"LAX": 337, "SEA": 679, "DEN": 967, "PHX": 651},
    "MIA": {"ATL": 594, "JFK": 1090, "CLT": 651, "IAH": 964},
    "BOS": {"JFK": 187, "ORD": 867, "PHL": 280},
    "PHX": {"DEN": 602, "LAX": 370, "SFO": 651},
    "IAH": {"DFW": 224, "MIA": 964, "ATL": 689},
    "CLT": {"ATL": 226, "MIA": 651, "JFK": 541},
    "SLC": {"DEN": 391, "SEA": 689, "SFO": 599},
    "MSP": {"ORD": 334, "DEN": 680, "SEA": 1399},
    "PHL": {"BOS": 280, "JFK": 94, "ATL": 666},
    "PDX": {"SEA": 129, "SFO": 550, "LAX": 834},
    "DTW": {"ORD": 235, "JFK": 509, "ATL": 594},
    "BWI": {"JFK": 184, "ATL": 576, "MIA": 946}
}

#creates a directed graph that contains the nodes and edges of the nested dict (flights)
flight_graph = nx.DiGraph()
for airport in flights:
    for destination, distance in flights[airport].items():
        flight_graph.add_edge(airport, destination, weight = distance)

'''Displays the visual representation of the flight graph'''
def display_visual_flight_paths(flight_graph):
    node_positions = nx.spring_layout(flight_graph)
    nx.draw(flight_graph, pos = node_positions, edge_color = "blue", width = 1, with_labels = True, arrows = True)
    plt.show()

'''Displays all the available flights from each airport and the distance to travel'''
def display_flight_paths(flights):

    print("\nAvaliable Flights: ")

    for airports, destinations in flights.items():

        flight_paths = []

        for destination, distance in destinations.items():
            flight_paths.append(f"{airports} -> {destination}: {distance}")

        print(f"{airports}: [{", ".join(flight_paths)}]")

'''Finds the shortest route of the given source and destination'''
def dijkstra(start, end):

    if start not in flights or end not in flights:
        print("Invalid Airport Code")
        return

    distances = {airport: float('inf') for airport in flights}
    distances[start] = 0
    visited = set()
    previous_visited = {}

    while len(visited) < len(flights):

        current_node = None
        smallest_distance = float('inf')

        #goes through all airports to find the closest unvisited airport
        for node in flights:
            if node not in visited and distances[node] < smallest_distance:
                smallest_distance = distances[node]
                current_node = node

        if current_node is None:
            break

        if current_node == end:
            break

        visited.add(current_node)

        #Finds all the outgoing flights from the current airport
        for neighbor, distance in flights[current_node].items():
            if neighbor not in visited:
                new_distance = distances[current_node] + distance

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_visited[neighbor] = current_node

    if distances[end] == float('inf'):
        print(f"There does not exist a path from {start} to {end}")
        return

    path = []
    current = end

    while current != start:
        path.append(current)
        current = previous_visited[current]

    path.append(start)
    path.reverse()

    print(f"{" -> ".join(path)}")
    print(f"The shortest path from {start} to {end}: {distances[end]} miles")

'''Identifies the top 5 most incoming and outgoing flights'''
def identify_hubs():
    incoming = {}
    outgoing = {}

    for airport in flights:
        incoming[airport] = 0
        outgoing[airport] = 0

    for airport in flights:
        for destination in flights[airport]:
            outgoing[airport] += 1
            incoming[destination] += 1


    highest_outgoing = dict(sorted(outgoing.items(), key = lambda x: x[1], reverse = True))
    highest_incoming = dict(sorted(incoming.items(), key = lambda x: x[1], reverse = True))

    print("Top 5 airports with the most outgoing flights: ")
    for i, (airport, connections) in enumerate(highest_outgoing.items()):
        if i == 5:
            break
        print(f"{airport} - {connections} outgoing flights")

    print("\nTop 5 airports with most incoming flights: ")
    for i, (airport, connections) in enumerate(highest_incoming.items()):
        if i == 5:
            break
        print(f"{airport} - {connections} incoming flights")

'''Finds the unreachable airports from the given airport'''
def find_unreachable(graph, source):
    if source not in graph:
        print("Invalid Airport Code")
        return
    
    reachable = nx.descendants(graph, source)
    reachable.add(source)

    unreachable = set(graph.nodes()) - reachable

    if len(unreachable) == 0:
        print(f"There are no unreachable airports from {source}")
    else:
        print(f"Unreachable airports from {source}: {unreachable}")

'''Displays the user interface where user is given the option to choose an action'''
def main():

    while True:

        print("======================")
        print("Flight Route Planner")
        print("======================")
        print("1. Display Visual Flight Graph")
        print("2. Display Available Airports")
        print("3. Find Shortest Route")
        print("4. Identify Airport Hubs")
        print("5. Find Unreachable Airports")
        print("6. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.\n")
            continue

        if (choice == 1):
            display_visual_flight_paths(flight_graph)
            print("")
        elif (choice == 2):
            display_flight_paths(flights)
            print("")

        elif (choice == 3):
            starting_choice = input("Enter the outgoing airport: ")
            destination_choice = input("Enter the destination airport: ")
            dijkstra(starting_choice, destination_choice)
            print("")

        elif (choice == 4):
            identify_hubs()
            print("")

        elif (choice == 5):
            unreachable_choice = input("Enter the airport code to find unreachable airports: ")
            find_unreachable(flight_graph, unreachable_choice)
            print("")

        elif (choice == 6):
            break
        else:
            print("Invalid Option\n")


main()




