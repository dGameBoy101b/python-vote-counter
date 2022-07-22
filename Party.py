class Party:
    '''A party that can be voted for'''
    
    def __init__(self, name:str):
        '''Construct a party with the given name
    name: The string name of the new party'''
        self.name = str(name)
        return

    def __repr__(self)->str:
        return f'Party({self.name!r})'

    def __str__(self)->str:
        return self.name

    def __eq__(self, other)->bool:
        return isinstance(other, Party) and self.name == other.name

    def __ne__(self, other)->bool:
        return not (self == other)

    def __hash__(self)->int:
        return hash(self.name)

if __name__ == '__main__':
    assert Party('labor').name == 'labor'
    assert repr(Party('labor')) == 'Party(' + repr('labor') + ')'
    assert str(Party('labor')) == 'labor'
    assert Party('labor') == Party('labor')
    assert Party('labor') != Party('liberal')
    assert hash(Party('labor')) == hash('labor')
    
    
