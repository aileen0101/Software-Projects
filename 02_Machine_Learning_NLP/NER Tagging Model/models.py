# Name(s): Aileen Huang
# Netid(s): aeh245
################################################################################
# NOTE: Do NOT change any of the function headers and/or specs!
# The input(s) and output must perfectly match the specs, or else your 
# implementation for any function with changed specs will most likely fail!
################################################################################

################### IMPORTS - DO NOT ADD, REMOVE, OR MODIFY ####################
from collections import defaultdict
from nltk import classify
from nltk import download
from nltk import pos_tag
import numpy as np

class HMM: 

  def __init__(self, documents, labels, vocab, all_tags, k_t, k_e, k_s, smoothing_func): 
    """
    Initializes HMM based on the following properties.

    Input:
      documents: List[List[String]], dataset of sentences to train model
      labels: List[List[String]], NER labels corresponding the sentences to train model
      vocab: List[String], dataset vocabulary
      all_tags: List[String], all possible NER tags 
      k_t: Float, add-k parameter to smooth transition probabilities
      k_e: Float, add-k parameter to smooth emission probabilities
      k_s: Float, add-k parameter to smooth starting state probabilities
      smoothing_func: (Float, Dict<key Tuple[String, String] : value Float>, List[String]) ->
      Dict<key Tuple[String, String] : value Float> 
    """
    self.documents = documents
    self.labels = labels
    self.vocab = vocab
    self.all_tags = all_tags
    self.k_t = k_t
    self.k_e = k_e
    self.k_s = k_s
    self.smoothing_func = smoothing_func
    self.emission_matrix = self.build_emission_matrix()
    self.transition_matrix = self.build_transition_matrix()
    self.start_state_probs = self.get_start_state_probs()


  def build_transition_matrix(self):
    """
    Returns the transition probabilities as a dictionary mapping all possible
    (tag_{i-1}, tag_i) tuple pairs to their corresponding smoothed 
    log probabilities: log[P(tag_i | tag_{i-1})]. 
    
    Note: Consider all possible tags. This consists of everything in 'all_tags', 
    but also 'qf' our end token. Use the `smoothing_func` and `k_t` fields to 
    perform smoothing.

    Note: The final state "qf" can only be transitioned into, there should be no 
    transitions from 'qf' to any other tag in your matrix

    Output: 
      transition_matrix: Dict<key Tuple[String, String] : value Float>
    """
    # YOUR CODE HERE
    print(self.all_tags, "all tags")

    all_our_tags = self.all_tags + ["qf"]

    #Build count of NER tag pairs (t, t-1)
    #Need to account for tag pairs (t, qf)
    ner_pair_counts = {}
    for tag in self.all_tags:
        for tag1 in all_our_tags:
            ner_pair_counts[(tag, tag1)] = 0 
    
    N = len(self.documents)
    for i in range(N):
        doc = self.documents[i]
        ner = self.labels[i]
        n = len(doc)
        for j in range(1, n):
            if j == n-1:
                #Last word
                pair = (ner[j], "qf")
                #...
                ner_pair_counts[pair] = ner_pair_counts.get(pair, 0) + 1
                
            pair = (ner[j-1], ner[j])
            ner_pair_counts[pair] = ner_pair_counts.get(pair, 0) + 1

    print("ner pair counts", ner_pair_counts)    
    
    return self.smoothing_func(self.k_t, ner_pair_counts, all_our_tags)

  def build_emission_matrix(self): 
    """
    Returns the emission probabilities as a dictionary, mapping all possible 
    (tag, token) tuple pairs to their corresponding smoothed log probabilities: 
    log[P(token | tag)]. 
    
    Note: Consider all possible tokens from the list `vocab` and all tags from 
    the list `all_tags`. Use the `smoothing_func` and `k_e` fields to perform smoothing.

    Note: The final state "qf" is final, as such, there should be no emissions from 'qf' 
    to any token in your matrix (this includes a special end token!). This means the tag 
    'qf' should not have any emissions, and thus not appear in your emission matrix.
  
    Output:
      emission_matrix: Dict<key Tuple[String, String] : value Float>
      Its size should be len(vocab) * len(all_tags).
    """
    # YOUR CODE HERE
      
    #Need to create a (word, tag) counter for all vocab, tag pairs
    observation_counts = {}
    valid_tags = [tag for tag in self.all_tags if tag != "qf"]
    for tag in valid_tags:
        for word in self.vocab:
            observation_counts[(tag, word)] = 0

    N = len(self.documents)
    for i in range(N):
        doc = self.documents[i]
        ner = self.labels[i]
        for j in range(len(doc)):
            tag = ner[j]
            if tag != "qf":
                word = doc[j]
                observation_counts[(tag, word)] += 1
    print(self.vocab, observation_counts.keys(), "emission count vocab vs keys")

    emission_matrix = self.smoothing_func(self.k_e, observation_counts, self.vocab)
      

    return emission_matrix


  def get_start_state_probs(self):
    """
    Returns the starting state probabilities as a dictionary, mapping all possible 
    tags to their corresponding smoothed log probabilities. Use `k_s` smoothing
    parameter to manually perform smoothing.
    
    Note: Do NOT use the `smoothing_func` function within this method since 
    `smoothing_func` is designed to smooth state-observation counts. Manually
    implement smoothing here.

    Note: The final state "qf" can only be transitioned into, as such, there should be no 
    transitions from 'qf' to any token in your matrix. This means the tag 'qf' should 
    not be able to start a sequence, and thus not appear in your start state probs.

    Output: 
      start_state_probs: Dict<key String : value Float>
    """
    # YOUR CODE HERE 

    # Want: P(tag as start) = # of tag, start + k/ total # of start tags + # of possible start tags * k 
    #Take log of this

    #Want: dictionary of tag : log(P(tag as start)
    valid_tags = [tag for tag in self.all_tags if tag != "qf"]
    total_unique_start = len(valid_tags)
    
    tag_starter_prob = {}
    
    #Initialize to 0 first
    for tag in valid_tags:
        tag_starter_prob[tag] = 0
    
    #Get count of each start tag first 
    N = len(self.documents)
    for i in range(N):
        if not self.labels[i]:
            continue
        start_tag = self.labels[i][0]
        tag_starter_prob[start_tag] = tag_starter_prob[start_tag] +1

    total_starts = sum(tag_starter_prob.values())
    #Compute probabilities
    denominator = total_starts + self.k_s * total_unique_start
    for tag in valid_tags:
        numerator = tag_starter_prob[tag] + self.k_s
        prob = numerator / denominator
        tag_starter_prob[tag] = np.log(prob)
    
    return tag_starter_prob

  def get_tag_likelihood(self, predicted_tag, previous_tag, document, i): 
    """
    Returns the tag likelihood used by the Viterbi algorithm for the label 
    `predicted_tag` conditioned on the `previous_tag` and `document` at index `i`.
    
    For HMM, this would be the sum of the smoothed log emission probabilities and 
    log transition probabilities: 
    log[P(predicted_tag | previous_tag))] + log[P(document[i] | predicted_tag)].
    
    Note: Treat unseen tokens as an <unk> token.
    
    Note: Make sure to handle the case where we are dealing with the first word. Is there a transition probability for this case?
    
    Note: Make sure to handle the case where predicted_tag is 'qf'. This corresponds to predicting the last token for a sequence. 
    We can transition into this tag, but (as per our emission matrix spec), there should be no emissions leaving. 
    As such, our probability when predicted_tag = 'qf' should merely be log[P(predicted_tag | previous_tag))].
  
    Input: 
      predicted_tag: String, predicted tag for token at index `i` in `document`
      previous_tag: String, previous tag for token at index `i` - 1
      document: List[String]
      i: Int, index of the `document` to compute probabilities 
    Output: 
      result: Float
    """
    # YOUR CODE HERE 
    #print("DOCUMENT", document)
    if predicted_tag == "qf":
        return self.transition_matrix.get((previous_tag, "qf"), float('-inf'))

    if i < len(document):
        token = document[i]
        if token not in self.vocab:
            token = "<unk>"
    else:
        token = "<unk>"

    if i == 0:
        log_transition = self.start_state_probs.get(predicted_tag, float('-inf'))
    else:
        log_transition = self.transition_matrix.get((previous_tag, predicted_tag), float('-inf'))

    log_emission = self.emission_matrix.get((predicted_tag, token), float('-inf'))

    return log_transition + log_emission
