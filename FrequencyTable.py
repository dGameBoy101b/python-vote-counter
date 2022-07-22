class FrequencyTable:
    '''A collection of values compressed into a frequency table'''

    def __init__(self, table:dict=dict()):
        '''Initialiser constructor
    table: The frequency table to copy'''
        self.table = dict()
        for key in table:
            if isinstance(table[key], (float, int)) and table[key] > 0:
                self.table[key] = float(table[key])
        return

    def __repr__(self)->str:
        return f'FrequencyTable({self.table!r})'

    def __str__(self)->str:
        return '\n'.join([f'{key}\t{self.table[key]}' for key in self.table])

    def __eq__(self, other)->bool:
        return isinstance(other, FrequencyTable) and self.table == other.table

    def add(self, item, frequency:float=1):
        '''Add the given value to the collection'''
        if isinstance(frequency, int):
            frequency = float(frequency)
        if not isinstance(frequency, float):
            raise TypeError(f'Frequencies must be a number, not a {type(frequency)}')
        if item not in self.table:
            self.table[item] = 0
        self.table[item] += frequency
        return

    def remove(self, item, frequency:float=1):
        '''Remove the given value to the collection'''
        if isinstance(frequency, int):
            frequency = float(frequency)
        if not isinstance(frequency, float):
            raise TypeError(f'Frequencies must be numbers, not {type(frequency)}')
        if frequency < 0:
            raise ValueError(f'Frequencies must be greater than 0, not {frequency}')
        if item not in self.table:
            return
        self.table[item] -= frequency
        if self.table[item] <= 0:
            del self.table[item]
        return

    def __getitem__(self, item)->float:
        '''Get the frequency of the given value'''
        if item not in self.table:
            self.table[item] = 0
        return self.table[item]

    def __setitem__(self, item, frequency:float):
        if isinstance(frequency, int):
            frequency = float(frequency)
        if not isinstance(frequency, float):
            raise TypeError(f'Frequencies can only be numbers, not {type(value)}')
        if frequency < 0:
            raise ValueError(f'Frequencies must be greater than 0, not {value}')
        if frequency == 0:
            if item in self.table:
                del self.table[item]
            return
        self.table[item] = frequency
        return

    def __delitem__(self, item):
        del self.table[item]

    def __getattr__(self, name:str)->float:
        '''total_frequency: Get the total number of items represented in the collection'''
        if name == 'total_frequency':
            return sum(self.table.values())
        raise AttributeError(name)

    def __iter__(self)->iter:
        return iter(self.table)

    def __contains__(self, item)->bool:
        return item in self.table

if __name__ == '__main__':
    assert FrequencyTable({None:3,'abc':13,123:-1,(1,-1):[1,-1]}).table == {None:3,'abc':13}
    assert repr(FrequencyTable({None:3,'abc':13})) == 'FrequencyTable(' + repr({None:3.,'abc':13.}) + ')'
    assert str(FrequencyTable({None:3,'abc':13})) in ('None\t3.0\nabc\t13.0','abc\t13.0\nNone\t3.0')
    assert FrequencyTable({None:3,'abc':13}) == FrequencyTable({'abc':13,None:3})
    assert FrequencyTable({None:3,'abc':13}) != FrequencyTable({None:4,'abc':13})
    assert FrequencyTable({None:3,'abc':13})[None] == 3
    assert FrequencyTable({None:3,'abc':13})[123] == 0
    assert FrequencyTable({None:3,'abc':13}).total_frequency == 3+13
    test = FrequencyTable({None:3,'abc':13})
    assert id(iter(test)) == id(iter(test.table))
    test.add(None)
    assert test[None] == 4
    test.add(123)
    assert test[123] == 1
    test.remove('abc')
    assert test['abc'] == 12
    test.remove(123)
    assert test[123] == 0
