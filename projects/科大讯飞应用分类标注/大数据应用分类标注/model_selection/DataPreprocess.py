import tensorflow as tf
from tensorflow.contrib import learn
from gensim.models import Word2Vec,FastText

data_path = "../data_preprocess/train_data.csv"
corpus_file = "F:/corpus/zhwiki-corpus-{}.model"

def gen_embed_matrix(corpus_file,w2v_model='Word2Vec',):
    if w2v_model=='Word2Vec':
        model = Word2Vec.load(corpus_file.format('w2v'))
    elif w2v_model == 'FastText':
        model = FastText.load(corpus_file.format('fasttext'))
    vocab = model.wv.vocab
    return vocab


def data_preprocess(data_path):

    # define a text generator
    def gline_x(data_path):
        with open(data_path, 'r', encoding='utf8') as f:
            f.readline()  # skip headers
            for line in f:
                yield line.split(',')[1]

    text_lines = gline_x(data_path)

    lenth_list = [len(txt.split()) for txt in text_lines]
    max_document_length = max(lenth_list)

    vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length=max_document_length,
                                                              min_frequency=1,
                                                              vocabulary=None,
                                                              tokenizer_fn=None)
    text_lines = gline_x(data_path)  # 该行不能少，否则没有内容.上一个生成器gline_x已经到尾了.
    vocab_processor.fit(text_lines)

    vocab_length = len(vocab_processor.vocabulary_)
    print("vocab length:", vocab_length)  # 148587

    # vocab = list(vocab_processor.reverse([list(range(0,len(vocab_processor.vocabulary_)))]))
    # print('vocabulary:\n',vocab)

    # 定义一个对类别y进行one_hot的生成器
    num_classes = 126

    def gline_y(data_path):
        with open(data_path, 'r', encoding='utf8') as f:
            f.readline()  # skip headers
            for line in f:
                one_hot_y = [0] * 126
                current_class = int(eval(line.split(',')[2]))
                one_hot_y[current_class] = 1
                yield one_hot_y

    def gline_xy():
        while True:
            text_lines = gline_x(data_path)
            for x, y in zip(vocab_processor.transform(text_lines), gline_y(data_path)):
                yield x, y

    data = tf.data.Dataset.from_generator(gline_xy, (tf.int64, tf.int64))
    data = data.shuffle(len(lenth_list))
    data = data.batch(32)
    # data = data.prefetch(1)

    return data, vocab_processor, max_document_length


if __name__ == '__main__':
    data, _, _ = data_preprocess(data_path)
    iterator = data.make_initializable_iterator()
    next_element = iterator.get_next()

    with tf.Session() as sess:
        sess.run(iterator.initializer)
        for i in range(5):
            print('data batch 1', i)
            print(sess.run(next_element))
