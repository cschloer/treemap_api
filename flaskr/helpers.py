import itertools
from .auth0 import get_user_names

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

def add_usernames(obj):
    '''
    A function that adds a user_name field to every dictionary
    contained within obj that has a user_id field
    '''
    user_ids = list(set(get_user_ids_from_object(obj)))
    user_names = get_user_names(user_ids)
    return set_user_names_to_object(user_names, obj)

def get_user_ids_from_object(obj):
    if type(obj) is list:
        return itertools.chain(*[get_user_ids_from_object(item) for item in obj])
    if type(obj) is dict:
        user_id = []
        if 'user_id' in obj:
            user_id = [obj['user_id']]
        return itertools.chain(user_id, *[get_user_ids_from_object(value) for value in obj.values()])
    return []

def set_user_names_to_object(user_names, obj):
    if type(obj) is list:
        return [set_user_names_to_object(user_names, item) for item in obj]
    if type(obj) is dict:
        if 'user_id' in obj:
            obj['user_name'] = user_names[obj['user_id']]
        return {key: set_user_names_to_object(user_names, value) for key, value in obj.items()}
    return obj
