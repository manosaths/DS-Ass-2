#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 21:37:07 2019

@author: sathim
"""

from collections import deque, namedtuple
from os import path
import sys

# infinity is used as a initial distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

# File Names Specified
inputFileName = "inputPS3.txt"
outputFileName = 'outputPS3.txt'

# In the problem it is assumed delivery leaves the source at 10am
start_time = 10


def make_edge(start, end, cost=1):
    """
    Create a named tuple Edge from given start end and cost
    :param start: Start vertex of the Edge
    :param end: End vertex of the Edge
    :param cost: Cost function to traverse through the edge
    :return: a named tuple Edge
    """
    return Edge(start, end, cost)


class Graph:
    """
    This class represents Graph object
    Attributes:
    edges: List of Named tuple Edge list(namedtuple('Edge', 'start, end, cost'))
    """
    def __init__(self, edges):
        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        """
        This method convert Edges to list of unique vertices
        for example [1,2], [3,4]) into [1, 2, 3, 4]
        :return: A set of vertices from all the Edges of the graph object
        """
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    @property
    def neighbours(self):
        """
        Find neighbours with cost to reach them
        for example :
        {'a': set([('f', 140), ('b', 70), ('c', 90)])}
        :return: A dict with key as vertex and values a Set of neighbours with cost
        """
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))
        return neighbours

    def dijkstra(self, src, dest):
        """
        Algorithm to find shortest path in the given graph , start and destination vertex.
        :param src: Source Node to start
        :param dest: Destination node to reach
        :return: If shortest path found then shortest_path , distance
        if not found then empty list([]), -1
        """
        if (src in self.vertices) and (dest in self.vertices):

            # 1. Mark all nodes as unvisited and store them.
            # 2. Set the distance to zero for our source node 
            # 3. Set the distance to infinity for other nodes.
            distances = {vertex: inf for vertex in self.vertices}
            # 4. This is used to keep a track of the path taken
            previous_vertices = {
                vertex: None for vertex in self.vertices
            }
            distances[source] = 0
            vertices = self.vertices.copy()

            while vertices:
                # 5. Select the unvisited node with the smallest distance, 
                # 6. Make it as the current node now.
                current_vertex = min(
                    vertices, key=lambda vertex: distances[vertex])

                # 7. Stop, if the smallest distance 
                # among the unvisited nodes is infinity.
                if distances[current_vertex] == inf:
                    break
                # 8. If the current  node is the destination Node  then 
                # we can break as that remains the optimum distance to the destination
                if current_vertex == dest:
                    break

                # 9. Find unvisited neighbors for the current node 
                # 10. Calculate their distances through the current node.
                for neighbour, cost in self.neighbours[current_vertex]:
                    alternative_route = distances[current_vertex] + cost

                    # 11.  Update the distance if the newly calculated distance\is better
                    # 12. Update the previous node also
                    if alternative_route < distances[neighbour]:
                        distances[neighbour] = alternative_route
                        previous_vertices[neighbour] = current_vertex

                # 13. Mark the current node as visited 
                # and remove it from the unvisited set.
                vertices.remove(current_vertex)

            path_q = deque()
            # 14. Start from the destination and traverse the previous nodes 
            # until we reach the source to find the path
            current_vertex = dest
            while previous_vertices[current_vertex] is not None:
                path_q.appendleft(current_vertex)
                current_vertex = previous_vertices[current_vertex]
            if path_q:
                path_q.appendleft(current_vertex)
            distance_nodes = 0
            # 15. calculate the distance also
            for index in range(1, len(path_q)):
                for thing in self.edges:
                    if thing.start == path_q[index - 1] and thing.end == path_q[index]:
                        distance_nodes += thing.cost
            # Convert the queue into list to display the output
            paths_list = list(path_q)
            print "Shortest Path Is", paths_list
            return paths_list, distance_nodes
        else:
            return [], -1


def convert_dist_to_time(nodes_distance):
    """
    Convert the distance to hours and minutes required
    @param :nodes_distance: Distance between two nodes
    :return hour , min and (am or pm)
    """
    at_hour = nodes_distance // 60
    at_minutes = nodes_distance % 60
    at_hour = start_time + at_hour
    if at_hour > 12:
        am_or_pm = "pm"
        at_hour = at_hour % 12
    else:
        am_or_pm = "am"
    return at_hour, at_minutes, am_or_pm


if __name__ == '__main__':
    """
    Main method to read given input file , calculate shortest path and print shortest path.
    """
    if path.exists(inputFileName):
        print("Reading the Input File -> " + inputFileName + "\n")
        edge_list = []
        with open(inputFileName, "r") as ins:
            for line in ins:
                line = line.split('\n')[0]
                inputs = (line.split('/'))
                if len(inputs) == 3:
                    inputs[0] = inputs[0].rstrip()
                    inputs[0] = inputs[0].lstrip()
                    inputs[1] = inputs[1].rstrip()
                    inputs[1] = inputs[1].lstrip()
                    inputs[2] = inputs[2].rstrip()
                    inputs[2] = inputs[2].lstrip()
                    edge_list.append((inputs[0], inputs[1], int(inputs[2])))
                elif len(inputs) == 1:
                    inputs[0] = inputs[0].split('\n')[0]
                    source_dest = (inputs[0].split(':'))
                    if len(source_dest) == 2:
                        source_dest[0] = source_dest[0].rstrip()
                        source_dest[0] = source_dest[0].lstrip()
                        source_dest[1] = source_dest[1].rstrip()
                        source_dest[1] = source_dest[1].lstrip()
                        if source_dest[0] == "DC Node":
                            source = source_dest[1]
                        elif source_dest[0] == "WH Node":
                            destination = source_dest[1]

        print("Graph edge list Generated from the input file \n")
        graph = Graph(edge_list)
        print("Calculating the shortest path \n")
        (path_list, distance_between_nodes) = graph.dijkstra(source, destination)
        if distance_between_nodes != -1:
            print("Generating the Output File \n")
            (hour, minutes, am_pm) = convert_dist_to_time(distance_between_nodes)
            path_list_str = "[ "
            for path_node in path_list:
                path_list_str = path_list_str + path_node + " "
            path_list_str = path_list_str + "]"
            orig_stdout = sys.stdout
            f = open(outputFileName, 'w')
            sys.stdout = f
            print(
                        "Shortest route from DC '" + source + "' to reach Warehouse '" + destination + "' is  " + path_list_str)
            print("and it has minimum travel distance " + str(distance_between_nodes) + "km")
            print("it will take him " + str(distance_between_nodes) + " minutes to reach")
            print("Expected arrival time at the warehouse is " + str(hour) + ":" + str(minutes) + am_pm)
            sys.stdout = orig_stdout
            f.close()
            print "Output File Generated. -> ", outputFileName
        else:
            print("Either Source or Destination is not Valid")
    else:
        print("Input File Not Present")
