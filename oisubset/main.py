import argparse
import yaml
import os
import shutil
import sys
import pandas as pd

OUTPUT_DESCRIPTION_FILE_NAME = "class-descriptions.csv"
OUTPUT_ANNOTATION_FILE_NAME = "annotations-bbox.csv"


def main(config):
    # Create Output Directory
    if os.path.exists(config["output_dir"]):
        print("OUTPUT DIRECTORY ALREADY EXIST!!")
        remove_flag = input("Remove? Y/n: ")
        if remove_flag == "Y":
            shutil.rmtree(config["output_dir"])
        else:
            print("bye.")
            sys.exit()
    os.makedirs(config["output_dir"] + "images")

    # Read and write Class Description file
    class_df = pd.read_csv(config["class_description_file"], header=None, names=('LabelName', "ClassName"))
    class_df = class_df[class_df["ClassName"].isin(config["target_classes"])]
    class_df.to_csv(config["output_dir"] + OUTPUT_DESCRIPTION_FILE_NAME, index=False, header=None)

    # Read bbox annotation file
    bbox_df = pd.read_csv(config["annotation_bbox_file"])

    # Copy image files to output Directory
    result_bbox_df = pd.DataFrame(index=[], columns=bbox_df.columns)
    for label in class_df["LabelName"]:
        image_count = 0
        print("Current Target label: ", class_df[class_df["LabelName"] == label].values)

        target_bbox_df = bbox_df[bbox_df["LabelName"] == label]
        target_bbox_df.reset_index(drop=True)
        target_bbox_df = target_bbox_df[target_bbox_df.index < config["max_images_per_class"]]
        result_bbox_df = result_bbox_df.append(target_bbox_df)

        for image_name in set(target_bbox_df["ImageID"]):
            if image_count >= config["max_images_per_class"]:
                break

            if image_count % 1000 == 0:
                print("Copy file count:", image_count)
                print("Now copying ImageID:", image_name)

            shutil.copy(config["image_dir"] + image_name + ".jpg",
                        config["output_dir"] + "images/" + image_name + ".jpg")
            image_count += 1

    result_bbox_df.to_csv(config["output_dir"] + OUTPUT_ANNOTATION_FILE_NAME, index=False)
    print("Data Set Conversion is Succeed!: ", config["output_dir"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate subset of Open Images V4 dataset")
    parser.add_argument("-c", "--config", help="Path to config yaml file", type=str, required=True)

    args = parser.parse_args()
    config = yaml.load(open(args.config, "r"))

    main(config)
