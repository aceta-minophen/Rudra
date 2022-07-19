import numpy as np
from glob import glob
from os.path import basename
from sklearn.ensemble import RandomForestClassifier
from micromlgen import port
from sklearn.svm import SVC


def load_features(folder):
    dataset = None
    classmap = {}
    for class_idx, filename in enumerate(glob('%s/*.csv' % folder)):
        class_name = basename(filename)[:-4]
        classmap[class_idx] = class_name
        samples = np.loadtxt(filename, dtype=float, delimiter=',')
        labels = np.ones((len(samples), 1)) * class_idx
        samples = np.hstack((samples, labels))
        dataset = samples if dataset is None else np.vstack((dataset, samples))

    return dataset, classmap


def get_classifier(features):
    X, y = features[:, :-1], features[:, -1]

    return RandomForestClassifier(20, max_depth=10).fit(X, y)


features, classmap = load_features('dataset')
X, y = features[:, :-1], features[:, -1]
#clf = OneClassSVM(kernel="rbf", nu=0.5, gamma=0.1)
classifier = SVC(kernel='linear', gamma=0.1).fit(X, y)
c_code = port(classifier, classmap=classmap)
print(c_code)
