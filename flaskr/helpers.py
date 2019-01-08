def transform_species_votes(species_votes):
    ''' Transform species_votes from a list of votes to a sorted list of lists of votes '''
    vote_tally = {}
    for vote in species_votes:
        vote_dict = vote.to_dict() if type(vote) is not dict else vote
        species_id = vote_dict['species_id']
        if species_id not in vote_tally:
            vote_tally[species_id] = []
        vote_tally[species_id].append(vote_dict)
    return_list = []
    # Put the tallied votes into an array
    for species in vote_tally.values():
        return_list.append(species)
    # Sort the array by number of votes
    return_list.sort(key = lambda species: len(species), reverse=True)

    return return_list
