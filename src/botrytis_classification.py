import pandas as pd

def select_non_botrytis_plants(dataset, diseased, filtered):
    # Generate a dataset with non-diseased plants (healthy plants)
    dataset = pd.read_csv(dataset)
    no_botrytis_id = []
    for i in dataset["Unnamed: 0"]:
        count = dataset["count_CHM"][i]
        if count < 1:
            no_botrytis_id.append(dataset["plantID"][i])
    classifier = pd.DataFrame(no_botrytis_id)
    classifier["status"] = "noBOT"
    classifier.columns = ["plantID", "status"]
    classifier.to_csv(diseased)
    # If CHM is lower than 1 (no canopy) the plants is healthy
    new_dataset = dataset.drop(dataset[dataset["count_CHM"] < 1].index)
    if "Unnamed: 0" in new_dataset:
        new_dataset.drop(["Unnamed: 0"], axis=1, inplace=True)
    new_dataset.to_csv(filtered)

