# Name(s): Aileen Huang
# Netid(s): aeh245
# #NOTE: I had to reindent the function or else it stopped running on my notebook!
################################################################################
# NOTE: Do NOT change any of the function headers and/or specs!
# The input(s) and output must perfectly match the specs, or else your 
# implementation for any function with changed specs will most likely fail!
################################################################################

################### IMPORTS - DO NOT ADD, REMOVE, OR MODIFY ####################
import numpy as np

def viterbi(model, observation, tags):
    """
    Returns the model's predicted tag sequence for a particular observation.
    Use `get_tag_likelihood` method to obtain model scores at each iteration.

    Input: 
        model: HMM model
        observation: List[String]
        tags: List[String]
    Output:
        predictions: List[String]
    """

    #NOTE: I had to reindent the function or else it stopped running on my notebook!
    N = len(observation)
    if N == 0:
        return []
    
    # viterbi_matrix[i][t] = best log-probability for a path ending in tag t at position i
    # backpointer_matrix[i][t] = best previous tag (at position i-1) for reaching tag t at position i
    viterbi_matrix = [{} for _ in range(N)]
    backpointer_matrix = [{} for _ in range(N)]
    
    # Initialization: i = 0, use the start state (e.g., "<s>") as the previous tag
    for t in tags:
        score = model.get_tag_likelihood(t, "", observation, 0)
        viterbi_matrix[0][t] = score
        backpointer_matrix[0][t] = None  
    
    for i in range(1, N):
        for t in tags:
            max_score = float("-inf")
            best_prev = None
            for t_prev in tags:
                prev_score = viterbi_matrix[i-1][t_prev]
                current_score = model.get_tag_likelihood(t, t_prev, observation, i)
                total_score = prev_score + current_score
                if total_score > max_score:
                    max_score = total_score
                    best_prev = t_prev
            viterbi_matrix[i][t] = max_score
            backpointer_matrix[i][t] = best_prev

    best_final_score = float("-inf")
    best_final_tag = None
    for t in tags:
        score = viterbi_matrix[N-1][t]
        if score > best_final_score:
            best_final_score = score
            best_final_tag = t

    predictions = [None] * N
    predictions[N-1] = best_final_tag
    for i in range(N-1, 0, -1):
        predictions[i-1] = backpointer_matrix[i][predictions[i]]
    
    return predictions
