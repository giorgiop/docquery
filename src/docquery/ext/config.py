# coding=utf-8
# Copyright 2010, The Microsoft Research Asia LayoutLM Team authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" LayoutLM model configuration"""
from transformers import LayoutLMConfig


class LayoutLMTokenClassifierConfig(LayoutLMConfig):
    r"""
    This is the configuration class to store the configuration of a [`LayoutLMModel`], extended to include token classification
    constants. It is used to instantiate a LayoutLM model according to the specified arguments, defining the model architecture.
    Instantiating a configuration with the defaults will yield a similar configuration to that of the LayoutLM
    [microsoft/layoutlm-base-uncased](https://huggingface.co/microsoft/layoutlm-base-uncased) architecture.
    Configuration objects inherit from [`BertConfig`] and can be used to control the model outputs. Read the
    documentation from [`BertConfig`] for more information.
    Args:
        vocab_size (`int`, *optional*, defaults to 30522):
            Vocabulary size of the LayoutLM model. Defines the different tokens that can be represented by the
            *inputs_ids* passed to the forward method of [`LayoutLMModel`].
        hidden_size (`int`, *optional*, defaults to 768):
            Dimensionality of the encoder layers and the pooler layer.
        num_hidden_layers (`int`, *optional*, defaults to 12):
            Number of hidden layers in the Transformer encoder.
        num_attention_heads (`int`, *optional*, defaults to 12):
            Number of attention heads for each attention layer in the Transformer encoder.
        intermediate_size (`int`, *optional*, defaults to 3072):
            Dimensionality of the "intermediate" (i.e., feed-forward) layer in the Transformer encoder.
        hidden_act (`str` or `function`, *optional*, defaults to `"gelu"`):
            The non-linear activation function (function or string) in the encoder and pooler. If string, `"gelu"`,
            `"relu"`, `"silu"` and `"gelu_new"` are supported.
        hidden_dropout_prob (`float`, *optional*, defaults to 0.1):
            The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.
        attention_probs_dropout_prob (`float`, *optional*, defaults to 0.1):
            The dropout ratio for the attention probabilities.
        max_position_embeddings (`int`, *optional*, defaults to 512):
            The maximum sequence length that this model might ever be used with. Typically set this to something large
            just in case (e.g., 512 or 1024 or 2048).
        type_vocab_size (`int`, *optional*, defaults to 2):
            The vocabulary size of the `token_type_ids` passed into [`LayoutLMModel`].
        initializer_range (`float`, *optional*, defaults to 0.02):
            The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
        layer_norm_eps (`float`, *optional*, defaults to 1e-12):
            The epsilon used by the layer normalization layers.
        max_2d_position_embeddings (`int`, *optional*, defaults to 1024):
            The maximum value that the 2D position embedding might ever used. Typically set this to something large
            just in case (e.g., 1024).
        token_classification (`bool, *optional*, defaults to False):
            Whether to include an additional token classification head in question answering
        token_classifier_reduction (`str`, *optional*, defaults to "mean")
            # TODO
        token_classifier_constant (`float`, *optional*, defaults to 1.0)
            # TODO
    Examples:
    ```python
    >>> from transformers import LayoutLMModel, LayoutLMConfig
    >>> # Initializing a LayoutLM configuration
    >>> configuration = LayoutLMConfig()
    >>> # Initializing a model from the configuration
    >>> model = LayoutLMModel(configuration)
    >>> # Accessing the model configuration
    >>> configuration = model.config
    ```"""
    model_type = "layoutlm-tc"

    def __init__(
        self,
        # New stuff added for DocQuery
        token_classification=False,
        token_classifier_reduction="mean",
        token_classifier_constant=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.token_classification = token_classification
        self.token_classifier_reduction = token_classifier_reduction
        self.token_classifier_constant = token_classifier_constant
