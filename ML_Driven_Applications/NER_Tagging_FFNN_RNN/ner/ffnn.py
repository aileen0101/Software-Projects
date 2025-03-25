# AUTO-GENERATED (DO NOT MODIFY)
# NET IDS: AEH245

from dataclasses import dataclass

import torch
import torch.nn.functional as F
from torch import nn

from ner.nn.module import Module


class FFNN(Module):
    def __init__(self, embedding_dim: int, hidden_dim: int, output_dim: int, num_layers: int = 1) -> None:
        """
        A multi-layer feed-forward neural network that applies a linear transformation, followed by a ReLU
        nonlinearity, at each layer.

        Parameters
        ----------
        embedding_dim : int
            Number of dimensions of an input embedding.
        hidden_dim : int
            Number of dimensions for the hidden layer(s).
        output_dim : int
            Number of dimensions for the output layer.
        num_layers : int
            Number of hidden layers to initialize.
        """
        super().__init__()

        assert num_layers > 0

        # TODO-4-1
        # Define W, V
        #First input to hidden
        self.input_hidden = nn.Linear(embedding_dim, hidden_dim)   
        self.hidden_layers = nn.ModuleList()
        for i in range(num_layers-1):
            self.hidden_layers.append(nn.Linear(hidden_dim, hidden_dim))

        #Last hidden to output
        self.hidden_output = nn.Linear(hidden_dim, output_dim)
        # Define f(•) 
        #self.f = F.relu()
            
        # Initialize the W, V matrices
        self.apply(self.init_weights)

    def forward(self, embeddings: torch.Tensor) -> torch.Tensor:
        """
        Computes a forward pass through each of the network layers using the given input embeddings.

        Parameters
        ----------
        embeddings : torch.Tensor
            Input tensor of embeddings of shape ``(batch_size, max_length, embedding_dim)``.

        Returns
        -------
        torch.Tensor
            Output tensor resulting from forward pass of shape ``(batch_size, max_length, output_dim)``.
        """
        # TODO-4-2

        hidden = F.relu(self.input_hidden(embeddings))

        num_hidden_passes = len(self.hidden_layers)
        for i in range(num_hidden_passes): #has #layers - 1 weight transformations
            W = self.hidden_layers[i] #W goes from k to k + 1
            hidden = F.relu(W(hidden)) #Update hidden layer k to next hidden layer k+1

    
        logits = self.hidden_output(hidden)

        return logits