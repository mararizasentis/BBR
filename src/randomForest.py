from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pandas as pd
from sklearn.metrics import accuracy_score


def randomForestBotrytis(train, test, output):
    # Load the training and test datasets
    train_dataset = pd.read_csv(train)
    test_dataset = pd.read_csv(test)
    training = train_dataset.drop(["status", "Unnamed: 0_x", "Unnamed: 0_y"], axis=1)
    training_labels = train_dataset["status"]

    # Select which mode is desired: validation or test
    # If test, the next exception runs
    if "status" not in test_dataset:
        # Train the Random Forest Classifier
        forest = RandomForestClassifier(criterion='entropy',
                                        n_estimators=1000,
                                        random_state=8,
                                        n_jobs=4,
                                        max_depth=15)
        forest.fit(training, training_labels)
        # Predict for the unseen data
        y_pred = forest.predict(test_dataset)
        prediction = pd.DataFrame({"plantID":test_dataset["plantID"], 'Predicted': y_pred})
        # Save the prediction results into a CSV file
        prediction.to_csv(output)

    # If validation, the next exception runs
    else:
        testing = test_dataset.drop(["plantID", "status"], axis=1)

        testing_labels = test_dataset["status"]
        # Train the Random Forest Classsifier
        forest = RandomForestClassifier(criterion='entropy',
                                        n_estimators=100,
                                        random_state=8,
                                        n_jobs=4,
                                        max_depth=5)
        forest.fit(training, training_labels)
        # Predict for the unseen data
        y_pred = forest.predict(testing)
        # All the validation metrics are computed
        print(accuracy_score(testing_labels, y_pred))
        print(metrics.confusion_matrix(testing_labels, y_pred))
        prediction = pd.DataFrame({'Actual': testing_labels, 'Predicted': y_pred})
        print(prediction.head())
        prediction.to_csv(output)
        print(metrics.confusion_matrix(testing_labels, y_pred))
        print(metrics.classification_report(testing_labels, y_pred))
        print(metrics.accuracy_score(testing_labels, y_pred))

