from Party import Party

class RankedVote:
    '''A vote in which parties are ranked in an order of the voters choosing'''

    def __init__(self, parties:tuple=tuple()):
        self.parties = list()
        for party in parties:
            if not isinstance(party, Party):
                try:
                    party = Party(party)
                except:
                    raise TypeError(f'Only parties may be listed in a ranked vote, not a {type(party)}')
            if party in self.parties:
                raise ValueError(f'No duplicate parties may be listed in a ranked vote; a duplicate was found for {party!r}')
            self.parties.append(party)
        return

    def __repr__(self)->str:
        return f'RankedVote({self.parties!r})'

    def __str__(self)->str:
        return '\n'.join([f'{index+1}\t{self.parties[index]}' for index in range(len(self.parties))])

    def __eq__(self, other)->bool:
        return isinstance(other, RankedVote) and self.parties == other.parties

    def __len__(self)->int:
        return len(self.parties)

    def __getitem__(self, index:int)->Party:
        return self.parties[index]

    def __setitem__(self, index:int, value:Party):
        if not isinstance(value, Party):
            try:
                value = Party(value)
            except:
                raise TypeError(f'Ranked vote items may only be parties, not {type(value)}')
        if self.parties[index] == value:
            return
        if value in self.parties:
            raise ValueError(f'No duplicate parties may be listed in a ranked vote; a duplicate was found for {party!r}')
        self.parties[index] = value
        return

    def __delitem__(self, index:int):
        del self.parties[index]
        return

    def __iter__(self)->iter:
        return iter(self.parties)

    def __reversed__(self)->iter:
        return reversed(self.parties)

    def __contains__(self, value:Party)->bool:
        if not isinstance(value, Party):
            value = Party(value)
        return value in self.parties

    def __add__(self, other)->'RankedVote':
        return RankedVote(self.parties + other)

    def __radd__(self,other)->'RankedVote':
        return RankedVote(other + self.parties)

    def __iadd__(self, other)->'RankedVote':
        self = self + other
        return self

if __name__ == '__main__':
    assert RankedVote([Party('labor'),'liberal']).parties == [Party('labor'),Party('liberal')]
    assert repr(RankedVote(['labor','liberal'])) == 'RankedVote(' + repr([Party('labor'),Party('liberal')]) + ')'
    assert str(RankedVote(['labor','liberal'])) == '1\tlabor\n2\tliberal'
    assert RankedVote(['labor','liberal']) == RankedVote(['labor','liberal'])
    assert RankedVote(['labor','liberal']) != RankedVote(['labor'])
    assert RankedVote(['labor','liberal']) != RankedVote(['labor','liberal','greens'])
    assert RankedVote(['labor','liberal']) != RankedVote(['labor','greens'])
    assert len(RankedVote(['labor','liberal'])) == 2
    assert RankedVote(['labor','liberal'])[0] == Party('labor')
    assert RankedVote(['labor','liberal'])[-1] == Party('liberal')
    assert RankedVote(['labor','liberal','greens'])[1:] == [Party('liberal'),Party('greens')]
    test = RankedVote(['labor','liberal'])
    test[1] = 'greens'
    assert test[1] == Party('greens')
    del test[0]
    assert len(test) == 1
    assert test[0] == Party('greens')
    assert test + ['labor','liberal'] == RankedVote(['greens','labor','liberal'])
    assert ['labor','liberal'] + test == RankedVote(['labor','liberal','greens'])
    test += ['labor','liberal']
    assert test == RankedVote(['greens','labor','liberal'])
    assert id(iter(test)) == id(iter(test.parties))
    assert id(reversed(test)) == id(reversed(test.parties))
    assert 'labor' in RankedVote(['labor','liberal'])
    assert Party('liberal') in RankedVote(['labor','liberal'])
    assert 'greens' not in RankedVote(['labor','liberal'])
    assert 7 not in RankedVote(['labor','liberal'])
