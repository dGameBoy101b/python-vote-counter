from Party import Party

class PreferentialVote:
    '''A preferential vote'''

    def __init__(self, parties:tuple=tuple()):
        self.parties = list()
        for party in parties:
            if isinstance(party, str):
                party = Party(party)
            if isinstance(party, Party) and party not in self.parties:
                self.parties.append(party)
        return

    def __repr__(self)->str:
        return f'PreferentialVote({self.parties!r})'

    def __str__(self)->str:
        return '\n'.join([f'{index+1}\t{self.parties[index]}' for index in range(len(self.parties))])

    def __eq__(self, other)->bool:
        return isinstance(other, PreferentialVote) and self.parties == other.parties

    def __len__(self)->int:
        return len(self.parties)

    def __getitem__(self, index:int)->Party:
        return self.parties[index]

    def __setitem__(self, index:int, value:Party):
        if isinstance(value, str):
            value = Party(value)
        if not isinstance(value, Party):
            raise TypeError(f'Preferential vote items may only be parties, not {type(value)}')
        if self.parties[index] == value:
            return
        if value in self.parties:
            raise ValueError(f'Each party may only be voted on once in a preferiential vote')
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
        if isinstance(value, str):
            value = Party(value)
        return value in self.parties

    def __add__(self, other)->'PreferentialVote':
        for party in other:
            if isinstance(party, str):
                party = Party(party)
            if not isinstance(party, Party):
                del party
        return PreferentialVote(self.parties + other)

    def __radd__(self,other)->'PreferentialVote':
        for party in other:
            if isinstance(party, str):
                party = Party(party)
            if not isinstance(party, Party):
                del party
        return PreferentialVote(other + self.parties)

    def __iadd__(self, other)->'PreferentialVote':
        for party in other:
            if isinstance(party, str):
                party = Party(party)
            if isinstance(party, Party) and party not in self.parties:
                self.parties.append(party)
        return self

if __name__ == '__main__':
    assert PreferentialVote([Party('labor'),'liberal','labor',7]).parties == [Party('labor'),Party('liberal')]
    assert repr(PreferentialVote(['labor','liberal'])) == 'PreferentialVote(' + repr([Party('labor'),Party('liberal')]) + ')'
    assert str(PreferentialVote(['labor','liberal'])) == '1\tlabor\n2\tliberal'
    assert PreferentialVote(['labor','liberal']) == PreferentialVote(['labor','liberal'])
    assert PreferentialVote(['labor','liberal']) != PreferentialVote(['labor'])
    assert PreferentialVote(['labor','liberal']) != PreferentialVote(['labor','liberal','greens'])
    assert PreferentialVote(['labor','liberal']) != PreferentialVote(['labor','greens'])
    assert len(PreferentialVote(['labor','liberal'])) == 2
    assert PreferentialVote(['labor','liberal'])[0] == Party('labor')
    assert PreferentialVote(['labor','liberal'])[-1] == Party('liberal')
    assert PreferentialVote(['labor','liberal','greens'])[1:] == [Party('liberal'),Party('greens')]
    test = PreferentialVote(['labor','liberal'])
    test[1] = 'greens'
    assert test[1] == Party('greens')
    del test[0]
    assert len(test) == 1
    assert test[0] == Party('greens')
    assert test + ['labor','liberal','greens',5] == PreferentialVote(['greens','labor','liberal'])
    assert ['labor','liberal','greens',5] + test == PreferentialVote(['labor','liberal','greens'])
    test += ['labor','liberal','greens',5]
    assert test == PreferentialVote(['greens','labor','liberal'])
    assert id(iter(test)) == id(iter(test.parties))
    assert id(reversed(test)) == id(reversed(test.parties))
    assert 'labor' in PreferentialVote(['labor','liberal'])
    assert Party('liberal') in PreferentialVote(['labor','liberal'])
    assert 'greens' not in PreferentialVote(['labor','liberal'])
    assert 7 not in PreferentialVote(['labor','liberal'])
