# Name(s): Aileen Huang
# Netid(s): aeh245
################################################################################
# NOTE: Do NOT change any of the function headers and/or specs!
# The input(s) and output must perfectly match the specs, or else your 
# implementation for any function with changed specs will most likely fail!
################################################################################

################### IMPORTS - DO NOT ADD, REMOVE, OR MODIFY ####################
import numpy as np
from viterbi import viterbi

def flatten_double_lst(lstlst):
   '''
   Returns flattened list version of double nested list (row-major)
   Input: 
    lstlst: List[List[Any]]
   Output:
    lst: List[Any]
   e.g: if lstlst = [[1,2], [3,4]]
        flatten_double_lst(lstlst) returns [1,2,3,4]
   '''
   return [element for lst in lstlst for element in lst]


def format_output_labels(token_labels, token_indices):
    """
    Returns a dictionary that has the labels (LOC, ORG, MISC or PER) as the keys,
    with the associated value being the list of entities predicted to be of that key label.
    Each entity is specified by its starting and ending position indicated in [token_indices].
    Input:
      token_labels: List[String], A list of token labels (eg. B-PER, I-PER, B-LOC, I-LOC, B-ORG, I-ORG, B-MISC, OR I-MISC).
      token_indices: List[Int], A list of token indices (taken from the dataset) corresponding to the labels in [token_labels].
    Output:
      result: Dictionary<key String: value List[Tuple]>, mapping labels to indices that have those labels
    Eg. if [token_labels] = ["B-ORG", "I-ORG", "O", "O", "B-ORG"]
           [token_indices] = [15, 16, 17, 18, 19]
        then dictionary returned is
        {'LOC': [], 'MISC': [], 'ORG': [(15, 16), (19, 19)], 'PER': []}
    """
    label_dict = {"LOC":[], "MISC":[], "ORG":[], "PER":[]}
    prev_label = 'O'
    start = token_indices[0]
    for idx, label in enumerate(token_labels):
      curr_label = label.split('-')[-1]
      if label.startswith("B-") or (curr_label != prev_label and curr_label != "O"):
        if prev_label != "O":
            label_dict[prev_label].append((start, token_indices[idx-1]))
        start = token_indices[idx]
      elif label == "O" and prev_label != "O":
        label_dict[prev_label].append((start, token_indices[idx-1]))
        start = None

      prev_label = curr_label
    if start is not None and prev_label != 'O':
      label_dict[prev_label].append((start, token_indices[idx]))
    return label_dict


def mean_f1(y_pred_dict, y_true_dict):
    """
    Calculates the entity-level mean F1 score given the actual/true and
    predicted span labels.
    Input:
      y_pred_dict: Dict<key String : value List[Tuple]>, a dictionary containing predicted labels as keys 
                                      and the list of associated span labels as the corresponding values.
      y_true_dict: Dict<key String : value List[Tuple]>, a dictionary containing true labels as keys 
                                      and the list of associated span labels as the corresponding values.
    Output:
      mean_f1_score: float, representing mean f1 score between truth values and preds
    Implementation modified from original by author @shonenkov at
    https://www.kaggle.com/shonenkov/competition-metrics.
    """
    F1_lst = []
    for key in y_true_dict:
        num_correct, num_true = 0, 0
        preds = y_pred_dict[key]
        trues = y_true_dict[key]
        for true in trues:
            num_true += 1
            if true in preds:
                num_correct += 1
            else:
                continue
        num_pred = len(preds)
        if num_true != 0:
            if num_pred != 0 and num_correct != 0:
                R = num_correct / num_true
                P = num_correct / num_pred
                F1 = 2*P*R / (P + R)
            else:
                F1 = 0      # either no predictions or no correct predictions
        else:
            continue
        F1_lst.append(F1)
    return np.mean(F1_lst)


def evaluate_model(model, val_set, tags):
  """
  Evaluates the model on the validation set `val_tokens` and `val_labels` and 
  returns the mean F1 score. Use provided helper function `mean_f1` to compare 
  predicted vs. actual labels.
  Input: 
    model: HMM model
    val_set: Dictionary<key String, value List[List[Any]]>, given validation set with keys: 'text', 'NER', 'index'
    tags: List[String], all possible NER tags 
  Output:
    mean_F1_score: Float, representing the mean f1 score when the model evaluated using the validation set
  """
  # YOUR CODE HERE 

  #Test our validation set with given HMM Model -> solve with Viterbi
  predicted_labels = []  
  for sentence in val_set['text']:
      pred = viterbi(model, sentence, tags)
      predicted_labels.append(pred)

  flat_predicted = flatten_double_lst(predicted_labels)
  flat_true = flatten_double_lst(val_set['NER'])
  flat_indices = flatten_double_lst(val_set['index'])

  #Code Reused from Assignment Instructions
  y_pred_dict = format_output_labels(flat_predicted, flat_indices)
  y_true_dict = format_output_labels(flat_true, flat_indices)
  print(compare_entity_dicts(y_pred_dict, y_true_dict)) #helper function to compare the outputs
  
  mean_F1_score = mean_f1(y_pred_dict, y_true_dict)




  return mean_F1_score


def compare_entity_dicts(y_pred, y_true):
    """
    Compares the predicted entity spans to the true entity spans for each entity type
    """
    differences = {}
    for label in y_true.keys():
        true_spans = set(y_true.get(label, []))
        pred_spans = set(y_pred.get(label, []))
        
        false_negatives = true_spans - pred_spans  # missed entities
        false_positives = pred_spans - true_spans  # extra entities predicted
        
        differences[label] = {
            'false_negatives': false_negatives,
            'false_positives': false_positives
        }
    return differences