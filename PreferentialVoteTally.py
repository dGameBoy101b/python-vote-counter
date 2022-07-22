from PreferentialVote import PreferentialVote
from FrequencyTable import FrequencyTable

class PreferentialVoteTally:
    '''A tally of preferential votes'''

    def __init__(self):
        self._vote_tree = dict()
        return

    def add_vote(self, vote:PreferentialVote):
        if isinstance(vote[0], str):
            vote = PreferentialVote(vote)
        if not isinstance(vote, PreferentialVote):
            raise TypeError(f'Can only add preferential votes, not {type(vote)}')
        tree = self._vote_tree
        for party in vote:
            if party not in tree:
                tree[party] = Node()
            tree[party].total_votes += 1
            tree = tree[party].children
        return

    def __getattr__(self, name):
        if name == 'total_votes':
            total_votes = 0
            for child in self.children:
                total_votes += child.total_votes
            return total_votes
        raise AttributeError(f'object has no attribute {name!r}')

    def assign_seats(self, num_seats:int)->FrequencyTable:
        if not isinstance(num_seats, int):
            raise TypeError(f'The number of seats must be an integer, not a {type(num_seats)}')
        if num_seats < 1:
            raise ValueError(f'The number of seats must be greater than 0, not {num_seats}')
        total_votes = self.total_votes
        threshold = total_votes / num_seats
        seats = FrequencyTable()
        tally = FrequencyTable()
        for party in self._vote_tree:
            tally[party] = self._vote_tree[party].total_votes
        while len(seats) < num_seats:
            majority_party = None
            for party in tally:
                if majority_party == None or tally[party] > tally[majority_party]:
                    majority_party = party
            if tally[majority_party] >= threshold or tally.total_frequency <= (num_seats - len(seats)) * threshold:
                seats.add(majority_party)
                tally.remove(majority_party, threshold)
                continue
            minority_frequency = None
            minority_parties = list()
            for party in tally:
                if minority_frequency == None or tally[party] < minority_frequency:
                    minority_frequency = tally[party]
                    minority_parties = [party]
                if tally[party] == minority_frequency:
                    minority_parties.append(party)
            nodes = []
            for party in minority_parties:
                del tally[party]
                nodes.append(self._vote_tree[party])
            while len(nodes) > 0:
                for party in nodes[0].children:
                    if party in tally:
                        tally.add(party, nodes[0].children[party].total_votes)
                    else:
                        nodes.append(nodes[0].children[party])
                del nodes[0]
        return seats
