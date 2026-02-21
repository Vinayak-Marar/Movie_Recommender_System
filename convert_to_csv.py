import csv

# dat_file_path = 'your_file.dat'
# csv_file_path = 'output_file.csv'
# delimiter_char = ' ' # Change this to your file's actual delimiter, e.g., ',' or '|'

# # Read the .dat file and write to a new .csv file

def convert_to_csv(dat_file_path,csv_file_path,delimiter_char="::"):

    with open(dat_file_path, 'r', encoding='latin-1') as infile, \
        open(csv_file_path, 'w', newline='', encoding='utf-8') as outfile:
        
        writer = csv.writer(outfile)
        
        for line in infile:
            # Strip whitespace and split by the double colon
            parts = line.strip().split(delimiter_char)
            
            # Write the parts as a standard CSV row
            writer.writerow(parts)

    print(f"Successfully converted {dat_file_path} to {csv_file_path}")



if __name__=="__main__":
    files = ["movies","ratings","users"]

    for file in files:
        convert_to_csv(f"data/{file}.dat",f"data/{file}.csv")