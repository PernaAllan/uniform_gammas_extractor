import os
import tarfile
import time

# Define file paths and directories
archive_path = "/lustre06/project/6084498/dnn/data/all_gammas.tgz"

# Target directories
base_group_dir = "/lustre06/project/6084498/dnn/data/uniform_gammas_base_group"
fvgains_dir = "/lustre06/project/6084498/dnn/data/uniform_gammas_base_group_FVGains"
noel_dir = "/lustre06/project/6084498/dnn/data/uniform_gammas_noel"
noel_fvgains_dir = "/lustre06/project/6084498/dnn/data/uniform_gammas_noel_FVGains"

# Ensure the directories exist
os.makedirs(base_group_dir, exist_ok=True)
os.makedirs(fvgains_dir, exist_ok=True)
os.makedirs(noel_dir, exist_ok=True)
os.makedirs(noel_fvgains_dir, exist_ok=True)


# Log file setup
log_file_path = "/lustre06/project/6084498/aperna/uniform_gammas_extractor/logs/uniform_gammas_extractor.txt"
log_file = open(log_file_path, "w")

# Custom print function to log and display progress
def log_print(message):
    print(message)  # Print to terminal
    log_file.write(message + "\n")


# Function to determine target directory
def get_target_directory(filename):
    if filename.startswith("./cut_gammas/"):
        return None
    
    if "noel" in filename and "fvgains.rpk" in filename:
        return noel_fvgains_dir
    elif "noel" in filename:
        return noel_dir
    elif "fvgains.rpk" in filename:
        return fvgains_dir
    else:
        return base_group_dir
        

# Extract and save the first two files
with tarfile.open(archive_path, "r:gz") as tar:
    #count = 0
    for member in tar:
        #if count >= 2:  # Stop after processing the first 2 files
            #break
        
        if member.isfile():  # Ensure it's a file, not a directory
            
            target_dir = get_target_directory(member.name)

            # Skip files that should not be extracted
            if target_dir is None:
                log_print(f"Skipping {member.name} (excluded by filter)")
                continue
            
            # Construct output path
            output_path = os.path.join(target_dir, os.path.basename(member.name))

            start_time = time.time() # Measure time taken for this file

            print(f"Output path is: {output_path}")
            
            # Extract the file to the target directory
            with tar.extractfile(member) as source_file:
                with open(output_path, "wb") as target_file:
                    target_file.write(source_file.read())

            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # print(f"Extracted {member.name} to {target_dir}")
            log_print(f"Extracted {member.name} to {target_dir} in {elapsed_time:.2f} seconds")
            #count += 1

# Close the log file

log_print(f"Log file saved at {log_file_path}")
log_file.close()


