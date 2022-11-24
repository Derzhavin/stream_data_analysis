from BERT.BERTGRUSentiment import BERTGRUSentiment

import torch
from transformers import BertTokenizer, BertModel
from typing import List


class SentimentEstimator:
    HIDDEN_DIM = 128
    OUTPUT_DIM = 1
    N_LAYERS = 1
    BIDIRECTIONAL = True
    DROPOUT = 0.25

    def __init__(self, model_path: str, target_device: str = 'cuda'):
        self.__device = torch.device(target_device)
        self.__model = BERTGRUSentiment(
                        BertModel.from_pretrained('bert-base-uncased'),
                         self.HIDDEN_DIM,
                         self.OUTPUT_DIM,
                         self.N_LAYERS,
                         self.BIDIRECTIONAL,
                         self.DROPOUT).to(self.__device)

        self.__model.load_state_dict(torch.load(model_path))
        self.__model.eval()
        self.__tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        init_token = self.__tokenizer.cls_token
        eos_token = self.__tokenizer.sep_token
        pad_token = self.__tokenizer.pad_token
        unk_token = self.__tokenizer.unk_token

        self.__max_input_length = self.__tokenizer.max_model_input_sizes['bert-base-uncased']

        self.__init_token_idx = self.__tokenizer.convert_tokens_to_ids(init_token)
        self.__eos_token_idx = self.__tokenizer.convert_tokens_to_ids(eos_token)
        self.__pad_token_idx = self.__tokenizer.convert_tokens_to_ids(pad_token)
        self.__unk_token_idx = self.__tokenizer.convert_tokens_to_ids(unk_token)

    def predict(self, sentences: List[str]) -> List[float]:
        indexed_sentences = []
        for sent in sentences:
            tokens = self.__tokenizer.tokenize(sent)
            tokens = tokens[:self.__max_input_length - 2]
            indexed = [self.__init_token_idx] + self.__tokenizer.convert_tokens_to_ids(tokens) + [self.__eos_token_idx]
            indexed_sentences += [indexed]

        tensor = torch.stack([torch.LongTensor(indexed) for indexed in indexed_sentences]).to(self.__device)
        prediction= torch.sigmoid(self.__model(tensor).squeeze()).tolist()

        if len(sentences) == 1:
            prediction = [prediction]

        return prediction


