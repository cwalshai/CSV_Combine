import os, glob
import csv
from tqdm import tqdm

VERSION="0.1"

def check_headers_match(file_list):
    file_count=0
    reference_header = None
    bool_list = []

    for filename in file_list:
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            row1 = next(csv_reader)

            if file_count==0:
                reference_header = row1
                bool_list.append(True)
            else:
                all_true = True
                for idx, cell in enumerate(reference_header):
                    if cell != row1[idx]:
                        all_true=False
                if all_true:
                    bool_list.append(True)
                else:
                    bool_list.append(False)

        file_count+=1

    if all(bool_list):
        return True, reference_header
    else:
        return False, None

def combine_files(file_list, output_file, headers):

    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, "a", newline='') as output_csv:
        csv_writer = csv.writer(output_csv)
        csv_writer.writerow(headers)
        
        for filename in tqdm(file_list):
            with open(filename, "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                linecount=0
                for row in csv_reader:
                    if linecount!=0:
                        csv_writer.writerow(row)
                    linecount+=1


def run(input_dir, output_file):
    file_list = glob.glob("*.csv")
    file_path_list = [os.path.join(input_dir,x) for x in file_list]

    print("CSV Concatenate V{}\n----------------\n".format(VERSION))

    list_len = len(file_path_list)
    if list_len>0:
        match, headers = check_headers_match(file_path_list)

        if match:
            print("Headers match, continuing to concatenate {} files, please wait.\n".format(list_len))
        else:
            print("Headers do not match, check files for consistency.\n")
            exit(1)

        combine_files(file_path_list, output_file, headers)

        print("\nComplete!\nConcatenated files output to {}.".format(output_file))

    else:
        print("No files found to combine.")




if __name__ == "__main__":
    input_dir = "."
    output_file = "combined.csv"

    run(input_dir, output_file)

    input("\n\nPress return to exit...")