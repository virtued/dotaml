from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.cross_validation import cross_val_score
from sklearn import svm
import pickle
import numpy as np
import os

def train(X, Y, num_samples):
    print('Training using data from %d matches...' % num_samples)
    #clf = SGDClassifier(loss='log', penalty="elasticnet", class_weight="auto")
    #return clf.fit(X[0:num_samples], Y[0:num_samples])
    #return LogisticRegression(class_weight={1:0.6563, 0:0.3436}).fit(X[0:num_samples], Y[0:num_samples])
    clf = ExtraTreesClassifier(n_estimators=2, max_depth=None,
            min_samples_split=10, random_state=0)
    clf.fit(X[0:num_samples], Y[0:num_samples]);
    #scores = cross_val_score(clf, X, Y)
    #print("score: ", scores)
    return clf


def main():
    # Import the preprocessed training X matrix and Y vector
    preprocessed = np.load('train_752845.npz')
    X_train = preprocessed['X']
    Y_train = preprocessed['Y']
    print(sum(Y_train));

    model = train(X_train, Y_train, len(X_train))

    with open('model.pkl', 'wb') as output_file:
        pickle.dump(model, output_file)

if __name__ == "__main__":
    main()
