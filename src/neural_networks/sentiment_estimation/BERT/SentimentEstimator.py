from transformers import BertTokenizer, BertModel
from typing import List


import torch
from torch import nn


class BERTGRUSentiment(nn.Module):
    def __init__(self,
                 bert,
                 hidden_dim,
                 output_dim,
                 n_layers,
                 bidirectional,
                 dropout):

        super().__init__()

        self.bert = bert

        embedding_dim = bert.config.to_dict()['hidden_size']

        self.rnn = nn.GRU(embedding_dim,
                          hidden_dim,
                          num_layers=n_layers,
                          bidirectional=bidirectional,
                          batch_first=True,
                          dropout=0 if n_layers < 2 else dropout)

        self.out = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)

        self.dropout = nn.Dropout(dropout)

    def forward(self, text):

        # text = [batch size, sent len]

        with torch.no_grad():
            embedded = self.bert(text)[0]

        # embedded = [batch size, sent len, emb dim]

        _, hidden = self.rnn(embedded)

        # hidden = [n layers * n directions, batch size, emb dim]

        if self.rnn.bidirectional:
            hidden = self.dropout(torch.cat((hidden[-2, :, :], hidden[-1, :, :]), dim=1))
        else:
            hidden = self.dropout(hidden[-1, :, :])

        # hidden = [batch size, hid dim]

        output = self.out(hidden)

        # output = [batch size, out dim]

        return output


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
        indexed_sentences = self.__tokenizer.batch_encode_plus(
            sentences,
            max_length=self.__max_input_length,
            padding='longest',
            truncation=True,
            return_token_type_ids=False
        )['input_ids']

        tensor = torch.stack([torch.LongTensor(indexed) for indexed in indexed_sentences]).to(self.__device)
        prediction= torch.sigmoid(self.__model(tensor).squeeze()).tolist()

        if len(sentences) == 1:
            prediction = [prediction]

        return prediction


