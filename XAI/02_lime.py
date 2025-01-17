# %% Imports
from interpret import show
from interpret.blackbox import LimeTabular
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from utils import DataLoader

# %% Load and preprocess data
data_loader = DataLoader()
data_loader.load_dataset()
data_loader.preprocess_data()
# Split the data for evaluation
X_train, X_test, y_train, y_test = data_loader.get_data_split()
# Oversample the train data
X_train, y_train = data_loader.oversample(X_train, y_train)
print(X_train.shape)
print(X_test.shape)
X_train = X_train.applymap(lambda x: 1.0 if x == True else 0.0 if x == False else x)
X_test = X_test.applymap(lambda x: 1.0 if x == True else 0.0 if x == False else x)

# %% Fit blackbox model
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
print(f"F1 Score {f1_score(y_test, y_pred, average='macro')}")
print(f"Accuracy {accuracy_score(y_test, y_pred)}")

# %% Apply lime
# Initilize Lime for Tabular data
# Local interpretable model-agnostic explanations
lime = LimeTabular(model=rf,
                   #predict_fn=rf.predict_proba, 
                   data=X_train, 
                   random_state=1)
# Get local explanations
lime_local = lime.explain_local(X_test[-20:], 
                                y_test[-20:], 
                                name='LIME')

show(lime_local)
# TODO: Check CNN and more complex models

# %%