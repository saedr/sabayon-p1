from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF, StopWordsRemover, NGram, Word2Vec 
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline
import sys
from os import path

def append_train_label(document):
	for i in range(len(train_names.value)):
		if document[0] == train_names.value[i]:
			return document[0], document[1], int(train_labels.value[i])

def match_test_label(document):
	for i in range(len(test_names.value)):
		if document[0] == test_names.value[i]:
			return int(test_labels.value[i])

def remove_train_line_id(document):
	text = ''
	for word in document[1].split():
		if len(word) <= 2:
			text += word + ' '
	return document[0], text, document[2]

def remove_test_line_id(document):
	text = ''
	for word in document[1].split():
		if len(word) <= 2:
			text += word + ' '
	return document[0], text


#Spark Defaults
sc = SparkContext()
spark = SparkSession(sc)

#Training Set
data = sc.wholeTextFiles('../../data/bytes') #sys.argv[1]
fp = open('../dataset/files/X_small_train.txt')
train_names = fp.read().split()
file_path = 'file:' + path.realpath('../../data/bytes') + '/' #sys.argv[1]
for i in range(len(train_names)):
	train_names[i] = file_path + train_names[i] + '.bytes'

train_names = sc.broadcast(train_names)

#Training Labels
fp = open('../dataset/files/y_small_train.txt')
train_labels = sc.broadcast(fp.read().split())

#Convert Training Data into a Data Frame
train_data = data.filter(lambda x: x[0] in train_names.value)
train_data = train_data.map(append_train_label)
train_data = train_data.map(remove_train_line_id)
train_df = train_data.toDF(['id', 'text', 'label'])

#Testing Set
fp = open('../dataset/files/X_small_test.txt')
test_names = fp.read().split()
file_path = 'file:' + path.realpath('../../data/bytes') + '/' #sys.argv[1]
for i in range(len(test_names)):
	test_names[i] = file_path + test_names[i] + '.bytes'
test_names = sc.broadcast(test_names)

#Testing Labels
fp = open('../dataset/files/y_small_test.txt')
test_labels = sc.broadcast(fp.read().split())

#Convert Testing Data into a Data Frame
test_data = data.filter(lambda x: x[0] in test_names.value)
test_data = test_data.map(remove_test_line_id)
test_df = test_data.toDF(['id', 'text'])
matched_test_labels = test_data.map(match_test_label).collect()

#Training: Tokenize, W2V, Logistic Regression
tokenizer = Tokenizer(inputCol="text", outputCol="words")
remover = StopWordsRemover(inputCol='words', outputCol='filtered', stopWords=['??']) #, '00'])
ngram = NGram(n=2, inputCol='filtered', outputCol='ngrams')
hashingTF = HashingTF(inputCol="ngrams", outputCol="features") #, numFeatures=256)
#idf = IDF(inputCol='freqs', outputCol='features')
#word2vec = Word2Vec(inputCol='ngrams', outputCol='features')
rf = RandomForestClassifier(maxDepth=7)

#ML Pipeline Model
pipeline = Pipeline(stages=[tokenizer, remover, ngram, hashingTF, rf])
model = pipeline.fit(train_df)
#model.save('RF_Bigram_TF_8')
predictions = model.transform(test_df)

#Evaluate Model Accuracy
test_predictions = predictions.select('prediction').collect()
correct = 0
for i in range(len(test_predictions)):
	if test_predictions[i][0] == matched_test_labels[i]:
		correct += 1
print('RF Model Accuracy ', (correct / len(test_predictions)))