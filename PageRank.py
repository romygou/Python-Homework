import random
from functools import reduce
from utils import data_to_dictionary

class PageRankDiGraph(object):
    '''
    A simple class for representing directed links between states. 
    Constructs a dictionary of link for fast lookups from a list of input link tuples.
    '''
    def __init__(self, data):
        '''
        Initialize with a dictionary representing links via data_to_dictionary()
        Args: 
            data: list of tuples
        Returns:
            None
        '''
        self.data = data
        self.link_dict = data_to_dictionary(data)
        
    def __len__(self):
        '''
        Returns the number of edges in the graph as int
        '''
        return len(self.data) # I'm giving it to you - no need to change

    def get_nodes(self):
        '''
        Returns a list of all nodes in the graph
        Args:
            None
        Returns:
            List of string (list of all nodes in the graph)
        '''
        # I'm giving it to you - no need to change or understand
        sung_to = reduce(lambda x, y: x+y, self.link_dict.values())
        singer = list(self.link_dict.keys())
        
        # easy trick to turn a list with duplicates items into list without duplicate items 
        return list(set(sung_to + singer))

    def __contains__(self, item):
        '''
        Running this function should give True if the item is present in the graph and False otherwise
        Args:
            item: string
        Returns:
            True if the item is present in the graph. False otherwise
        '''
        return item in self.get_nodes()

    def __str__(self):
        '''
        Args:
            None
        Returns:
            "PageRankDiGraph with {number of nodes} nodes and {number of edges} edges."
        '''
        txt = "PageRankDiGraph with {} nodes and {} edges."
        return print(txt.format(len(self.get_nodes()), self.__len__()))

    def __add__(self, other):
        '''
        Combines two PageRankDiGraphs
        Args:
            other: A different instance of this class
        Returns:
            new instance of PageRankDiGraph that contains both the edges of this instance and other
        '''
        # hint: should be one line
        return self + other

    def linked_by(self, x):
        '''
        Return a list of states linked from x, with states listed multiple times if they are linked multiple times.
        Args:
            x: string (a node of the graph)
        Returns:
            list of string (nodes connected to the input)
        '''
        return self.link_dict[x]


class PageRankIterator(object):
    """
    A custom iterator class for performing approximate PageRank random walks through a PR_DiGraph. 
    """
    
    def __init__(self, graph, iteration_limit=20, jump_prob=0.85):
        '''
        When initialized, this class should create instance variables to store:
            - graph: the PageRankDiGraph instance, given as input
            - iteration_limit: an integer given as input
            - jump_prob: a float between 0 and 1 (inclusive), given as input
            - a counter 'iter': starting at 0, to log the number of steps taken
            - current_state: variable whose value is one of the keys of the 'link_dict' of the 'PageRankDiGraph'
        Args:
            graph: instance of PageRankDiGraph class
            iteration_limit: int (explained above)
            jump_prob: float (explained above)
        Returns:
            None
        '''
        if isinstance(graph, PageRankDiGraph):
            self.graph = graph
            self.iteration_limit = iteration_limit
            self.jump_prob = jump_prob
            self.iter = 0
            self.current_state = "hamilton"
        else:
            raise TypeError("Input graph is not an instance of PageRankDiGraph.")

    def follow_link(self):
        '''
        Follow a random directed link in self.D. Teleports if either the selected link links the state to itself, or 
        if there are no links from the current state.
        Args:
            None
        Returns:
            None
        '''
        try:
            self.current_values = self.graph.link_dict[self.current_state] #extract a list of values from dictionary
            self.next_state = random.choice(self.current_values) #pick a random new character mentioned by the current character
        
            if self.next_state != self.current_state:
                self.current_state = self.next_state #set current_state to next_state if next_state != current_state
            else:
                self.teleport() #teleport() if next_state == current_state
        except:
            self.teleport() #teleport() if there is a KeyError
    
    def teleport(self):
        '''
        Set the current state to a state uniformly at random, from the set of all possible states.
        Args:
            None
        Returns:
            None
        '''
        self.current_state = random.choice(self.graph.get_nodes()) #set a random node as current_state

    def __iter__(self):
        '''
        return the iterator object (self)
        '''
        return self

    def __next__(self):
        '''
        With probability self.p, follow the link relationship; otherwise teleport, until the iteration_limit is reached.
        Args:
            None
        Returns:
            the iterator's current state
        '''
        if self.iter <= self.iteration_limit: #continue if the counter has not surpassed iteration_limit
            if random.random() < self.jump_prob: #follow_link() with jump_prob% probability
                self.follow_link()
                self.iter += 1 #increase counter
            else: #teleport() with 1 - jump_prob% probability
                self.teleport()
                self.iter += 1 #increase counter
        else:
            raise StopIteration #stop iteration if the counter has surpassed iteration_limit
            
        return self.current_state


class IterablePageRankDiGraph(PageRankDiGraph):
    '''
    A subclass of PageRankDiGraph that inherits all of PageRankDiGraph's methods.
    '''
    def __init__(self, data, iteration_limit = 20, jump_prob = 0.75):
        '''
        Initialize with a dictionary representing links via data_to_dictionary().
        Args: 
            data: list of tuples
            iteration_limit: int, iteration limit given as input
            jump_prob: float, between 0 and 1 (inclusive) given as input
        Returns:
            None
        '''
        self.data = data
        self.link_dict = data_to_dictionary(data)
        self.iteration_limit = iteration_limit
        self.jump_prob = jump_prob

    def __str__(self):
        '''
        Args:
            None
        Returns:
            "IterablePageRankDiGraph with {number of nodes} nodes and {number of edges} edges."
        '''
        txt = "IterablePageRankDiGraph with {} nodes and {} edges."
        return print(txt.format(len(self.get_nodes()), self.__len__()))
    
    def __iter__(self):
        '''
        Returns:
            a new instance of PageRankIterator initialized with the IterablePageRankDiGraph instance and its iteration_limit and
            jump_prob values
        '''
        return PageRankIterator(IterablePageRankDiGraph(self.data))