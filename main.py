import glob, os, zipfile, pathlib, shutil
from tqdm import tqdm
import cv2

INPUT_FOLDER_NAME = "data"
UNPACK_FOLDER_NAME = "unpack"
OUTPUT_FOLDER_NAME = "output"
FOLDER_SEPARATOR = "\\"
IMAGE_FORMATS = ["jpg", "jpeg", "png"]
TQDM_BAR_FORMAT = "{l_bar}{bar:10}{r_bar}"
PAGE_NUMBER = 1


def clear_output_folder():
    files = glob.glob(f"{OUTPUT_FOLDER_NAME}/*")
    for f in files:
        os.remove(f)


def get_data_folder_files():
    types = ("*.cbz", "*.cbr")
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(f"{INPUT_FOLDER_NAME}/{files}"))
    return files_grabbed


def cut_image_in_half(image_path, image_folder_name):
    global PAGE_NUMBER

    # Read the image
    img = cv2.imread(image_path)
    height = img.shape[0]
    width = img.shape[1]

    # Cut the image in half
    width_cutoff = width // 2
    s1 = img[:, :width_cutoff]
    s2 = img[:, width_cutoff:]

    # Check if vol folder exists - if not, create it
    output_folder_content_names = list(
        map(
            lambda folder: folder.replace("\\", "/"),
            glob.glob(f"./{OUTPUT_FOLDER_NAME}/*"),
        )
    )
    output_folder_content_names = [
        element.split("/")[-1] for element in output_folder_content_names
    ]
    if image_folder_name not in output_folder_content_names:
        os.mkdir(f"./{OUTPUT_FOLDER_NAME}/{image_folder_name}")

    # Save each half
    save_path = f"./{OUTPUT_FOLDER_NAME}/{image_folder_name}/{image_folder_name}"
    cv2.imwrite(f"{save_path}_{PAGE_NUMBER}.jpg", s1)
    PAGE_NUMBER += 1
    cv2.imwrite(f"{save_path}_{PAGE_NUMBER}/.jpg", s2)


def manga_page_halfer():
    # Clear the output to avoid os errors
    clear_output_folder()

    # Get input paths
    data_folder_content = [
        element.split(FOLDER_SEPARATOR)[-1]
        for element in glob.glob(f"./{INPUT_FOLDER_NAME}/*")
    ]
    packed_files = get_data_folder_files()
    if not packed_files:
        print(
            "[ERROR] Could not find any CBR nor CBZ files in ./data/ folder. Exiting the script."
        )
        return
    unpack_folder_path = f"./{INPUT_FOLDER_NAME}/{UNPACK_FOLDER_NAME}"

    # Check if unpack folder exists - if it doesn't, then create one
    if UNPACK_FOLDER_NAME not in data_folder_content:
        os.mkdir(unpack_folder_path)

    for packed_file in tqdm(
        packed_files,
        desc="[INFO] Extracting and halving the images",
        bar_format=TQDM_BAR_FORMAT,
    ):
        global PAGE_NUMBER
        PAGE_NUMBER = 1  # os.walk behaves really weird, so there was no way to use local iterator - had to use global to store the number of page
        # Get paths
        file_name = " ".join(packed_file.split(".")[:-1]).split(FOLDER_SEPARATOR)[-1]
        extract_path = f"./{INPUT_FOLDER_NAME}/{UNPACK_FOLDER_NAME}/{file_name}"

        # Extract images from zips/rars
        with zipfile.ZipFile(packed_file, "r") as zip_ref:
            zip_ref.extractall(extract_path)

        # Go through the extarcted images and halve them
        for path, subdirs, files in os.walk(extract_path):
            for name in files:
                if name.endswith((".jpg", ".jpeg", ".gif", ".png")):
                    image_file_path = os.path.join(path, name)
                    image_folder_name = image_file_path.replace("\\", "/").split("/")[
                        image_file_path.replace("\\", "/")
                        .split("/")
                        .index(UNPACK_FOLDER_NAME)
                        + 1
                    ]
                    cut_image_in_half(image_file_path, image_folder_name)

    # Get output files
    output_volumes = glob.glob(f"./{OUTPUT_FOLDER_NAME}/*")

    # Go through each folder (from extracted zips/rars) and zip it to .cbz format
    for volume in tqdm(
        output_volumes,
        desc="[INFO] Converting (packing) extracted images to .cbz format",
        bar_format=TQDM_BAR_FORMAT,
    ):
        directory = pathlib.Path(volume)
        volume_name = volume.replace("\\", "/").split("/")[-1]
        with zipfile.ZipFile(
            f"{OUTPUT_FOLDER_NAME}/{volume_name} HALVED.cbz", mode="w"
        ) as archive:
            for file_path in directory.iterdir():
                archive.write(file_path, arcname=file_path.name)

        # Delete unpacked folder after ziping it
        shutil.rmtree(volume)


if __name__ == "__main__":
    manga_page_halfer()
