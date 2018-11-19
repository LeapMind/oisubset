import argparse
import yaml
import os
import shutil
import pandas as pd

OUTPUT_DESCRIPTION_FILE_NAME = "class-descriptions.csv"
OUTPUT_ANNOTATION_FILE_NAME = "annotations-bbox.csv"


def main(config):
    # Create Output Directory
    os.mkdir(config["output_dir"])
    os.mkdir(config["output_dir"] + "images")

    class_df = pd.read_csv(config["class_description_file"], header=None, names=('LabelName', "ClassName"))
    class_df = class_df[class_df["ClassName"].isin(config["target_classes"])]
    class_df.to_csv(config["output_dir"] + OUTPUT_DESCRIPTION_FILE_NAME, index=False, header=None)
    target_labels = class_df["LabelName"]

    bbox_df = pd.read_csv(config["annotation_bbox_file"])
    bbox_df = bbox_df[bbox_df["LabelName"].isin(target_labels)]
    bbox_df = bbox_df.reset_index(drop=True)
    bbox_df = bbox_df[bbox_df.index < config["max_images_per_class"]]
    bbox_df.to_csv(config["output_dir"] + OUTPUT_ANNOTATION_FILE_NAME, index=False)

    # Copy image files to output Directory
    image_count = 0
    for image_name in set(bbox_df["ImageID"]):
        if image_count % 1000 == 0:
            print("Copy count:", image_count)
            print("Now copying ImageID:", image_name)

        shutil.copy(config["image_dir"] + image_name + ".jpg", config["output_dir"] + "images/" + image_name + ".jpg")
        image_count += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate subset of Open Images V4 dataset")
    parser.add_argument("-c", "--config", help="Path to config yaml file", type=str, required=True)

    args = parser.parse_args()
    config = yaml.load(open(args.config, "r"))

    main(config)
