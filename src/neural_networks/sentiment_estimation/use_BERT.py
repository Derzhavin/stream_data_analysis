from BERT import SentimentEstimator


if __name__ == '__main__':
    sentences = [
        "This film is terrible",
        "This film is great",
    ] * 1024

    p = SentimentEstimator(model_path='./sentiment_estimation_BERT.pt')

    results = p.predict(sentences)

    for i in range(len(sentences)):
        print(sentences[i], results[i])