from BERT import SentimentEstimator
import time

if __name__ == '__main__':
    sentences = [
        "This film is very terrible",
        "This film is great",
    ] * 2

    p = SentimentEstimator(model_path='./sentiment_estimation_BERT.pt')
    p.predict(sentences[:1])

    t_begin = time.time()
    results = p.predict(sentences)
    t_diff = (time.time() - t_begin) * 1000

    for i in range(len(sentences)):
        print(sentences[i], results[i])

    print(t_diff)