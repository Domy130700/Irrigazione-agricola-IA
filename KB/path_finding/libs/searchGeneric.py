from KB.path_finding.libs.display import Displayable, visualize
import heapq
from itertools import count

class Arc(object):
    def __init__(self, from_node, to_node, cost=1, action=None):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost
        self.action = action

class Search_problem(object):
    def start_node(self): raise NotImplementedError
    def is_goal(self, node): raise NotImplementedError
    def neighbors(self, node): raise NotImplementedError
    def heuristic(self, n): return 0

class Path(object):
    def __init__(self, initial, arc=None):
        self.initial = initial
        self.arc = arc
        if arc is None:
            self.cost = 0
        else:
            self.cost = initial.cost + arc.cost

    def end(self):
        if self.arc is None: 
            return self.initial
        else: 
            return self.arc.to_node

    def nodes(self):
        current = self
        res = []
        while current.arc is not None:
            res.append(current.arc.to_node)
            current = current.initial
        res.append(current.initial)
        return res[::-1]

def AStarsearch(problem):
    """
    Motore dell'algoritmo A* con tie-breaker per evitare il TypeError su Path
    """
    frontier = []
    counter = count()  # contatore unico per tie-breaking
    start_path = Path(problem.start_node())
    heapq.heappush(frontier, (start_path.cost + problem.heuristic(start_path.end()), next(counter), start_path))
    
    explored = set()
    
    while frontier:
        _, _, path = heapq.heappop(frontier)
        node = path.end()
        
        if node not in explored:
            explored.add(node)
            
            if problem.is_goal(node):
                return path
            
            for arc in problem.neighbors(node):
                new_path = Path(path, arc)
                heapq.heappush(frontier, (new_path.cost + problem.heuristic(new_path.end()), next(counter), new_path))
    
    return None
