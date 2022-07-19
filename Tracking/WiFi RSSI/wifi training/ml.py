from sklearn.svm import SVC
from micromlgen import port

# put your samples in the dataset folder
# one class per file
# one feature vector per line, in CSV format
features, classmap = load_features('dataset/')
X, y = features[:, :-1], features[:, -1]
classifier = SVC(kernel='linear').fit(X, y)
c_code = port(classifier, classmap=classmap)
print(c_code)
