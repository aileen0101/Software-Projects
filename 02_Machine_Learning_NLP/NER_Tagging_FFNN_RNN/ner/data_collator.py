# AUTO-GENERATED (DO NOT MODIFY)
# NET IDS: AEH245

import logging
from dataclasses import dataclass
from typing import Union, Optional, List, Dict, Any

import numpy as np
import torch

from ner.data_processing.constants import NER_ENCODING_MAP, PAD_NER_TAG
from ner.data_processing.tokenizer import Tokenizer


class DataCollator(object):
    def __init__(
        self,
        tokenizer: Tokenizer,
        padding: Union[str, bool] = "longest",
        max_length: Optional[int] = None,
        padding_side: str = "right",
        truncation_side: str = "right",
        pad_tag: str = PAD_NER_TAG,
        text_colname: str = "text",
        label_colname: str = "NER",
    ):
        
        """
        Creates a data collator to collate batches of data instances into dictionaries with the strings ``"input_ids"``,
        ``"padding_mask"``, and ``"labels"`` (if not test data) as keys and associated tensors as values.

        Parameters
        ----------
        tokenizer : :py:class:`~ner.data_processing.tokenizer.Tokenizer`
            The tokenizer to be used when tokenizing the data.
        padding : {True or "longest", "max_length", False}, default: "longest"
            Indicates the padding strategy for the tokenizer. If "longest" or True, then pad to the longest sequence
            in the batch; if "max_length" and ``max_length`` argument is not None, pad to the specified ``max_length``;
            if False, don't pad.
        max_length : Optional[int], default: None
            The maximum length to pad to, when specified, ``padding = "longest"`` will be ignored in favor of
            ``padding = "max_length"``.
        padding_side : {"left", "right"}, default: "right"
            Indicates which side to pad the batch input sequences on.
        truncation_side : {"left", "right"}, default: "right"
            Indicates which side to truncate the batch input sequences on.
        pad_tag : str, default: :py:const:`~ner.data_processing.constants.PAD_NER_TAG`
            The label (NER tag) associated with the padding tokens.
        text_colname : str, default: "text"
            The name of the column in the arrow dataset that contains the text (sequence of tokens).
        label_colname : str, default: "NER"
            The name of the column in the arrow dataset that contains the NER labels.
        """

        self.tokenizer = tokenizer
        self.padding = padding
        self.max_length = max_length
        self.padding_side = padding_side
        self.truncation_side = truncation_side
        self.pad_tag = pad_tag
        self.text_colname = text_colname
        self.label_colname = label_colname


    def _get_max_length(self, data_instances: List[Dict[str, Any]]) -> Optional[int]:
        """
        Depending on the :py:attr:`~ner.data_processing.data_collator.DataCollator.padding`, retrieves the length
        to pad to, if padding is being done.

        Parameters
        ----------
        data_instances : List[Dict[str, Any]]
            A list (batch) of training, validation, or test data instances.

        Returns
        -------
        Optional[int]
            The desired padding length, or None if no padding is being done.
        """

        if not ((self.padding == "longest" or self.padding) and self.max_length is None):
            logging.warning(
                f"both max_length={self.max_length} and padding={self.padding} provided; ignoring "
                f"padding={self.padding} and using max_length={self.max_length}"
            )
            self.padding = "max_length"

        if self.padding == "longest" or (isinstance(self.padding, bool) and self.padding):
            return max([len(data_instance[self.text_colname]) for data_instance in data_instances])
        elif self.padding == "max_length":
            return self.max_length
        elif isinstance(self.padding, bool) and not self.padding:
            return None
        raise ValueError(f"padding strategy {self.padding} is invalid")

    @staticmethod
    def _process_labels(labels: List) -> torch.Tensor:
        """
        Converts the string labels into a tensor of label IDs using
        :py:const:`~ner.data_processing.constants.NER_ENCODING_MAP`.

        Parameters
        ----------
        labels : List
            A list of NER labels corresponding to one data instance.

        Returns
        -------
        torch.Tensor
            A tensor of label IDs corresponding to ``labels``.
        """
        return torch.LongTensor([NER_ENCODING_MAP[label] for label in labels])

    def __call__(self, data_instances: List[Dict[str, Any]]) -> Dict[str, torch.Tensor]:
        """
        Tokenize and pad (if applicable) a list (batch) of data instances into a dictionary with the strings
        ``"input_ids"``, ``"padding_mask"``, and ``"labels"`` (if not test data) as keys and associated tensors as
        values.

        Parameters
        ----------
        data_instances : List[Dict[str, Any]]
            A list (batch) of training, validation, or test data instances.

        Returns
        -------
        Dict[str, torch.Tensor]
            A dictionary with strings ``"input_ids"``, ``"padding_mask"``, and ``"labels"`` (if not test data) as keys
            and associated batched tensors (batch size is ``len(data_instances)``) as values.
        """
        # TODO-1.2-1
        batch_size = len(data_instances)
        batch_max_len = self._get_max_length(data_instances)
        
        batch_input_ids = torch.empty((batch_size, batch_max_len), dtype=torch.long)
        batch_padding_mask = torch.empty((batch_size, batch_max_len), dtype=torch.long)
        
        has_labels = self.label_colname in data_instances[0]
        if has_labels:
            batch_labels = torch.empty((batch_size, batch_max_len), dtype=torch.long)
        
        for i, instance in enumerate(data_instances):
            text = instance[self.text_colname]
            tokenized = self.tokenizer.tokenize(
                text,
                max_length=batch_max_len,
                padding_side=self.padding_side,
                truncation_side=self.truncation_side
            )
            input_ids = tokenized["input_ids"].squeeze()
            padding_mask = tokenized["padding_mask"].squeeze()
            batch_input_ids[i] = input_ids
            batch_padding_mask[i] = padding_mask
            
            if has_labels:
                og_labels = instance[self.label_colname]
                if len(og_labels) < batch_max_len:
                    if self.padding_side == "right":
                        padded = og_labels + [self.pad_tag] * (batch_max_len - len(og_labels))
                    else:
                        padded = [self.pad_tag] * (batch_max_len - len(og_labels)) + og_labels
                elif len(og_labels) > batch_max_len:
                    if self.truncation_side == "left":
                        padded = og_labels[-batch_max_len:]
                    else:
                        padded = og_labels[:batch_max_len]
                else:
                    padded = og_labels

                labels_tensor = self._process_labels(padded)
                batch_labels[i] = labels_tensor

        result = {
            "input_ids": batch_input_ids,
            "padding_mask": batch_padding_mask,
        }
        if has_labels:
            result["labels"] = batch_labels
        return result


        

    