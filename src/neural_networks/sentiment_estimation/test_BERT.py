import torch
import torch.nn as nn
from torchtext.legacy import data
from torchtext.legacy import datasets
from transformers import BertTokenizer, BertModel
import random
import numpy as np

from BERT import BERTGRUSentiment

SEED = 1234

HIDDEN_DIM = 128
OUTPUT_DIM = 1
N_LAYERS = 1
BIDIRECTIONAL = True
DROPOUT = 0.25

BATCH_SIZE = 32

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.backends.cudnn.deterministic = True

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
torch.set_num_threads(6)
torch.set_num_interop_threads(6)


def binary_accuracy(preds, y):
    """
    Returns accuracy per batch, i.e. if you get 8/10 right, this returns 0.8, NOT 8
    """

    # round predictions to the closest integer
    rounded_preds = torch.round(torch.sigmoid(preds))
    correct = (rounded_preds == y).float()  # convert into float for division
    acc = correct.sum() / len(correct)
    return acc


def evaluate(model, iterator, criterion):
    epoch_loss = 0
    epoch_acc = 0

    model.eval()

    with torch.no_grad():
        for batch in iterator:
            predictions = model(batch.text).squeeze(1)

            loss = criterion(predictions, batch.label)

            acc = binary_accuracy(predictions, batch.label)

            epoch_loss += loss.item()
            epoch_acc += acc.item()

    return epoch_loss / len(iterator), epoch_acc / len(iterator)


if __name__ == '__main__':
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    init_token = tokenizer.cls_token
    eos_token = tokenizer.sep_token
    pad_token = tokenizer.pad_token
    unk_token = tokenizer.unk_token

    init_token_idx = tokenizer.convert_tokens_to_ids(init_token)
    eos_token_idx = tokenizer.convert_tokens_to_ids(eos_token)
    pad_token_idx = tokenizer.convert_tokens_to_ids(pad_token)
    unk_token_idx = tokenizer.convert_tokens_to_ids(unk_token)

    max_input_length = tokenizer.max_model_input_sizes['bert-base-uncased']

    def tokenize_and_cut(sentence):
        tokens = tokenizer.tokenize(sentence)
        tokens = tokens[:max_input_length - 2]
        return tokens

    TEXT = data.Field(batch_first=True,
                      use_vocab=False,
                      tokenize=tokenize_and_cut,
                      preprocessing=tokenizer.convert_tokens_to_ids,
                      init_token=init_token_idx,
                      eos_token=eos_token_idx,
                      pad_token=pad_token_idx,
                      unk_token=unk_token_idx)

    LABEL = data.LabelField(dtype=torch.float)


    train_data, test_data = datasets.IMDB.splits(TEXT, LABEL)
    print(f"Number of testing examples: {len(test_data)}")

    LABEL.build_vocab(train_data)

    # test_iterator = data.BucketIterator.splits(
    #     (test_data,),
    #     batch_size=BATCH_SIZE,
    #     device=device)
    test_iterator = data.BucketIterator(
        test_data,
        batch_size=BATCH_SIZE,
        device=device)

    criterion = nn.BCEWithLogitsLoss().to(device)

    model = BERTGRUSentiment(
        BertModel.from_pretrained('bert-base-uncased'),
        HIDDEN_DIM,
        OUTPUT_DIM,
        N_LAYERS,
        BIDIRECTIONAL,
        DROPOUT).to(device)

    model.load_state_dict(torch.load('sentiment_estimation_BERT.pt'))
    model.eval()
    model = model.to(device)

    test_loss, test_acc = evaluate(model, test_iterator, criterion)

    print(f'Test Loss: {test_loss:.3f} | Test Acc: {test_acc * 100:.2f}%')