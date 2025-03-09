import os
import re
import tarfile
#import logging

# TESTING FOR 5 FILES
MAX_FILES_TO_PROCESS = 5  # Adjust this number
processed_count = 0


tgz_path = "/lustre06/project/6084498/dnn/data/all_gammas.tgz"
#base_dir = "/lustre06/project/6084498/dnn/data/" #this is the common output directory
base_dir = '/lustre06/project/6084498/aperna/uniform_gammas_extractor/tests/test_output'


# logging.basicConfig(
#     filename = os.path.join(base_dir, 'test_uniform_gammas_organizer.log'),
#     level=logging.INFO,
#     format='%(asctime)s - %(message)s'
# )

categories = {
    "uniform_gammas_base_group": re.compile(r'^uniform_gammas/uniform_gammas_100k_group\d+\.hdf5$'),
    "uniform_gammas_base_group_FVGains": re.compile(r'^uniform_gammas/uniform_gammas_100k_group\d+_fvgains\.rpk\.hdf5$'),
    "uniform_gammas_noel": re.compile(r'^uniform_gammas/uniform_gammas_noel_100k_group\d+\.hdf5$'),
    "uniform_gammas_noel_FVGains": re.compile(r'^uniform_gammas/uniform_gammas_noel_100k_group\d+_fvgains\.rpk\.hdf5$')
}

try:
    #Creating output directories
    for dir_name in categories:
        os.makedirs(os.path.join(base_dir, dir_name), exist_ok=True)
    
    with tarfile.open(tgz_path, "r:gz") as tar:
        for member in tar:
    
            # TESTING
            
            if processed_count >= MAX_FILES_TO_PROCESS:
                break  # Stop after processing 5 files
    
            
            if not member.isfile() or not member.name.startswith('uniform_gammas/'):
                continue
    
            for dir_name, pattern in categories.items():
                if pattern.match(member.name):
                    target_name = os.path.basename(member.name)
                    target_path = os.path.join(base_dir, dir_name, target_name)
    
    
                    with open(target_path, 'wb') as f:
                        f.write(tar.extractfile(member).read()) # tar.extractfile(member): Extracts the file’s content as a stream (doesn’t load the entire archive into memory)
                                                                # read(): Reads the file’s bytes.
                                                                # f.write(...): Writes the bytes directly to the target directory.
                                                                # This avoids storing the entire archive or intermediate files on disk.
    
                    print(f"Extracted: {member.name} -> {target_path}")
                    #logging.info(f"Extracted: {member.name} -> {target_path}")
                    processed_count += 1
                    break


except Exception as e:
    #logging.error(f"Error: {str(e)}")
    print(f"Error: {str(e)}")







