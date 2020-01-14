import numpy as np

from backend.intent_classification.data_cleanup import cleaning, create_tokenizer, encoding_doc, \
    padding_doc, one_hot, word_tokenizer, cleaned_words, unique_intent, intent, vocab_size, max_length_cleaned_words

from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Bidirectional, Embedding, Dropout
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split


def write_set_to_file(filename, my_list):
    with open(filename, 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)


#Bideractional Gated recurrent unit algorithm (complex shit)
def create_model(vocab_size, max_length):
    model = Sequential()
    model.add(Embedding(vocab_size, 128, input_length=max_length, trainable=False))
    model.add(Bidirectional(LSTM(128)))
    model.add(Dense(32, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(3, activation="softmax"))

    return model


#run this to train!!!
encoded_doc = encoding_doc(word_tokenizer, cleaned_words)
padded_doc = padding_doc(encoded_doc, max_length_cleaned_words)

output_tokenizer = create_tokenizer(unique_intent, filters='!"#$%&()*+,-/:;<=>?@[\]^`{|}~')

encoded_output = encoding_doc(output_tokenizer, intent)
encoded_output = np.array(encoded_output).reshape(len(encoded_output), 1)

output_one_hot = one_hot(encoded_output)

print(output_one_hot.shape)

'''
Run this to train your model
'''
train_X, val_X, train_Y, val_Y = train_test_split(padded_doc, output_one_hot, shuffle=True, test_size=0.2)
model = create_model(vocab_size, max_length_cleaned_words)

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.summary()

filename = 'model.h5'
checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=1, save_best_only=True, mode='min')

hist = model.fit(train_X, train_Y, epochs=100, batch_size=32, validation_data=(val_X, val_Y), callbacks=[checkpoint])

