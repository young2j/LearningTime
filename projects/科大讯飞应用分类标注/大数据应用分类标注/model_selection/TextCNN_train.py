import tensorflow as tf
import os
import time
import datetime
from TextCNN import TextCNN
from DataPreprocess import data_preprocess


def train():
    # 指定样本文件
    data_file = "../data_preprocess/train_data.csv"

    # 设置训练参数
    num_steps = 2000
    display_every = 10
    checkpoint_every = 100
    save_file = 'textcnn'

    # 设置模型参数
    num_classes = 126
    dropout_keep_prob = 0.8
    l2_reg_lambda = 0.1
    filter_sizes = [3, 5, 7]
    num_filters = 256
    embedding_size = 128

    tf.reset_default_graph()

    # 预处理数据
    data, vocab_processor, max_document_length = data_preprocess(data_file)
    iterator = data.make_one_shot_iterator()
    next_element = iterator.get_next()

    # 定义cnn model
    cnn = TextCNN(
        sequence_length=max_document_length,
        num_classes=num_classes,
        vocab_size=len(vocab_processor.vocabulary_),
        embedding_size=embedding_size,
        filter_sizes=filter_sizes,
        num_filters=num_filters,
        l2_reg_lambda=l2_reg_lambda,
    )

    # 构建网络
    cnn.build_model()

    # 打开会话
    session_conf = tf.ConfigProto(
        allow_soft_placement=True, log_device_placement=False)
    with tf.Session(config=session_conf) as sess:
        sess.run(tf.global_variables_initializer())

        # 输出模型路径
        out_dir = os.path.abspath(os.path.join(os.path.curdir, save_file))
        print("Writing to {}\n".format(out_dir))

        # 设置输出摘要路径
        train_summary_dir = os.path.join(out_dir, "summaries")
        train_summary_writer = tf.summary.FileWriter(
            train_summary_dir, sess.graph)

        # 设置检查点文件名称
        checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
        checkpoint_prefix = os.path.join(checkpoint_dir, "model")

        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)

        # 定义操作检查点的Saver
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)

        # # 保存字典
        # vocab_processor.save(os.path.join(out_dir,"vocab"))

        def train_step(x_batch, y_batch):
            feed_dict = {
                cnn.input_x: x_batch,
                cnn.input_y: y_batch,
                cnn.dropout_keep_prob: dropout_keep_prob
            }
            _, step, summaries, loss, accuracy = sess.run(
                [cnn.train_op, cnn.global_step, cnn.train_summary_op, cnn.loss, cnn.accuracy], feed_dict)

            time_str = datetime.datetime.now().isoformat()
            train_summary_writer.add_summary(summaries, step)

            return (time_str, step, loss, accuracy)

        i = 0
        while tf.train.global_step(sess, cnn.global_step) < num_steps:
            x_batch, y_batch = sess.run(next_element)
            i += 1
            time_str, step, loss, accuracy = train_step(x_batch, y_batch)

            current_step = tf.train.global_step(sess, cnn.global_step)
            if current_step % display_every == 0:
                print("{}:step {},loss {:g},acc {:g}".format(
                    time_str, step, loss, accuracy))

            if current_step % checkpoint_every == 0:
                path = saver.save(sess, checkpoint_prefix,
                                  global_step=current_step)
                print("Saved model checkpoint to {}\n".format(path))

# def main(argv=None):
# 	train()

# if __name__=='__main__':
# 	tf.app.run()


if __name__ == '__main__':
    train()
