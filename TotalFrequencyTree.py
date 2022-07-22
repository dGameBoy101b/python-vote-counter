class TotalFrequencyTree:
    '''Stores lists of items in a frequency tree with the constraint that the frequency of a node must be at least the total of the child frequencies'''

    class Node:
        '''A node for a total frequency tree'''

        def __init__(self, total_frequency:float=0, children:dict=dict()):
            '''Initialiser constructor
    total_frequency: The positive total frequency of this node and its children (may be increased to match the calculated total frequency of the given children)
    children: The dictionary of children nodes'''
            if not isinstance(total_frequency, float):
                total_frequency = float(total_frequency)
            if total_frequency < 0:
                raise ValueError(f'Total frequency must be 0 or greater, not {total_frequency}')
            if not isinstance(children, dict):
                children = dict(children)
            total = 0
            for key in children:
                if not isinstance(children[key], TotalFrequencyTree.Node):
                    raise TypeError(f'Every value of children must be nodes, not a {type(children[key])}')
                total += children[key].total_frequency
            self.children = children
            self.total_frequency = max(total_frequency, total)
            return

        def __repr__(self)->str:
            return f'TotalFrequencyTree.Node({self.total_frequency!r},{self.children!r})'

        def __str__(self)->str:
            if len(self.children) > 0:
                return f'{self.total_frequency}\n' + '\n'.join([str(key) + '\n'.join([f'\t{line}' for line in str(self.children[key]).split('\n')]) for key in self.children])
            return str(self.total_frequency)

        def __eq__(self, other)->bool:
            return isinstance(other, TotalFrequencyTree.Node) and self.total_frequency == other.total_frequency and self.children == other.children

        def copy(self)->'Node':
            '''Create a shallow copy'''
            return TotalFrequencyTree.Node(self.total_frequency, self.children)

        def deep_copy(self)->'Node':
            '''Create a deep copy'''
            return TotalFrequencyTree.Node(self.total_frequency, dict([(key, self.children[key].deep_copy()) for key in self.children]))

    def __init__(self, root:Node=Node()):
        if not isinstance(root, Node):
            root = Node(root)
        self.root = root
        return

    def __repr__(self)->str:
        return f'TotalFrequencyTree({self.root!r})'

    def __str__(self)->str:
        return str(self.root)

    def __eq__(self, other)->bool:
        return isinstance(other, TotalFrequencyTree) and self.root == other.root

    def add(self, items:list, frequency:float=1):
        '''Add the given list of items to the tree with the given frequency'''
        if not isinstance(frequency, float):
            frequency = float(frequency)
        if frequency <= 0:
            raise ValueError(f'Frequency must be greater than 0, not {frequency}')
        node = self.root
        items = list(items)
        while len(items) > 0:
            node.total_frequency += frequency
            if items[0] not in node.chlidren:
                node.children[items[0]] = Node()
            node = node.children[items[0]]
            del items[0]
        return

    def remove(self, items:list, frequency:float=1):
        '''Remove the given list of items from the tree with the given frequency'''
        if not isinstance(frequency, float):
            frequency = float(frequency)
        if frequency <= 0:
            raise ValueError(f'Frequency must be greater than 0, not {frequency}')
        nodes = [self.root]
        for item in items:
            if item not in nodes[-1].children:
                raise KeyError(repr(items))
            nodes.append(nodes[-1].children[item])
        frequency = min(nodes[-1].total_frequency, frequency)
        for i in range(len(nodes)-1):
            nodes[i].total_frequency -= frequency
            if nodes[i+1].total_frequency < frequency:
                del nodes[i].children[items[i]]
                break
        return

    def clear(self):
        '''Clear all items from the tree'''
        self.root = Node()
        return

    def __contains__(self, keys:list)->bool:
        '''Check if a list of items that begins with the given list of items is in the tree'''
        node = self.root
        for key in keys:
            if ke not in node.children:
                return False
            node = node.children[key]
        return True

    def __getitem__(self, keys:list)->float:
        '''Get the frequency of all lists of items that begin with the given list of items'''
        node = self.root
        for key in keys:
            if key not in node.children:
                return 0
            node = node.children[key]
        return node.total_frequency

if __name__ == '__main__':
    assert TotalFrequencyTree.Node().total_frequency == 0
    assert TotalFrequencyTree.Node().children == dict()
    assert TotalFrequencyTree.Node(3).total_frequency == 3
    assert TotalFrequencyTree.Node(0,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)}).children == {'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)}
    assert TotalFrequencyTree.Node(54.2,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)}).total_frequency == 54.2
    assert TotalFrequencyTree.Node(0,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)}).total_frequency == 13+.4
    assert repr(TotalFrequencyTree.Node(0,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)})) == 'TotalFrequencyTree.Node('+repr(13+.4)+','+repr({'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)})+')'
    assert str(TotalFrequencyTree.Node(54,{'abc':TotalFrequencyTree.Node(13,{123:TotalFrequencyTree.Node(4.38)}),None:TotalFrequencyTree.Node(.4)})) == str(54.0)+'\n'+str('abc')+'\t'+str(13.0)+'\n\t'+str(123)+'\t'+str(4.38)+'\n'+str(None)+'\t'+str(0.4)
    assert TotalFrequencyTree.Node(0,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)}) == TotalFrequencyTree.Node(0,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)})
    assert TotalFrequencyTree.Node(54,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)}) != TotalFrequencyTree.Node(125,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)})
    assert TotalFrequencyTree.Node(54,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)}) != TotalFrequencyTree.Node(54,{'abc':TotalFrequencyTree.Node(13.2),None:TotalFrequencyTree.Node(.4)})
    assert TotalFrequencyTree.Node(54,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)}) != TotalFrequencyTree.Node(54,{None:TotalFrequencyTree.Node(.4)})
    assert TotalFrequencyTree.Node(54,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)}) != TotalFrequencyTree.Node(54,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4),123:TotalFrequencyTree.Node(8.3)})
    test_node = TotalFrequencyTree.Node(0,{'abc':TotalFrequencyTree.Node(13),None:TotalFrequencyTree.Node(.4)})
    assert test_node is not test_node.copy()
    assert test_node == test_node.copy()
    assert test_node.children is test_node.copy().children
    assert test_node is not test_node.deep_copy()
    assert test_node == test_node.deep_copy()
    assert test_node.children is not test_node.deep_copy().children
    del test_node
    
    
