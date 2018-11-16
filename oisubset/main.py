import argparse
import yaml
import os
import shutil
import csv
import pandas as pd

CLASS_DESCRIPTION_FILE_NAME = "class-descriptions.csv"


def main(config):
    # Create Output Directories
    os.mkdir(config["output_dir"])
    os.mkdir(config["output_dir"] + "/images")

    target_classes = []
    target_labels = []

    # Fetch class label names
    with open(config["class_description_file"], "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1] in config["target_classes"]:
                target_classes.append(row)
                target_labels.append(row[0])

    print("target_class_labels:", target_classes)

    # Write class description subset to csv
    with open(config["output_dir"] + CLASS_DESCRIPTION_FILE_NAME, "w") as csvfile:
        writer = csv.writer(csvfile, lineterminator="\n")
        writer.writerows(target_classes)

    df = pd.read_csv(config["annotation_bbox_file"])
    print("all df:\n", df)

    df = df[df["LabelName"].isin(target_labels)]
    df.to_csv(config["output_dir"] + "annotations-bbox.csv", index=False)
    print("selected df:\n", df)

    # Copy image files to output Directory
    for image_name in set(df["ImageID"]):
        print(image_name)
        shutil.copy(config["image_dir"] + image_name + ".jpg", config["output_dir"] + "images/" + image_name + ".jpg")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate subset of Open Images V4 dataset")
    parser.add_argument("-c", "--config", help="Path to config yaml file", type=str, required=True)

    args = parser.parse_args()
    config = yaml.load(open(args.config, "r"))

    main(config)
