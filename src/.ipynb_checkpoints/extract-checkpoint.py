# Nao ta dando certo

import tarfile
import os
import re

# Paths
TGZ_FILE = "/lustre06/project/6084498/dnn/data/all_gammas.tgz"
EXTRACT_DIR = "/lustre06/project/6084498/dnn/data/temp_extracted/"  # Temporary extraction location
DEST_DIRS = {
    "base": "/lustre06/project/6084498/dnn/data/uniform_gammas_base_group/",
    "noel": "/lustre06/project/6084498/dnn/data/uniform_gammas_noel/",
    "fvgains": "/lustre06/project/6084498/dnn/data/uniform_gammas_base_group_FVGains/",
    "noel_fvgains": "/lustre06/project/6084498/dnn/data/uniform_gammas_noel_FVGains/"
}

# Patterns to classify files
PATTERNS = {
    "base": re.compile(r"uniform_gammas_100k_group\d+\.hdf5$"),
    "noel": re.compile(r"uniform_gammas_noel_100k_group\d+\.hdf5$"),
    "fvgains": re.compile(r"uniform_gammas_100k_group\d+_fvgains\.rpk\.hdf5$"),
    "noel_fvgains": re.compile(r"uniform_gammas_noel_100k_group\d+_fvgains\.rpk\.hdf5$")
}

def extract_and_classify():
    """Extract relevant files from tar and move them to categorized directories."""
    # Ensure destination directories exist
    for dir_path in DEST_DIRS.values():
        os.makedirs(dir_path, exist_ok=True)
    
    with tarfile.open(TGZ_FILE, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.startswith("uniform_gammas/"):
                filename = os.path.basename(member.name)
                
                # Determine file category
                for category, pattern in PATTERNS.items():
                    if pattern.match(filename):
                        print(f"Extracting {filename} to {DEST_DIRS[category]}")
                        tar.extract(member, EXTRACT_DIR)
                        src_path = os.path.join(EXTRACT_DIR, member.name)
                        dest_path = os.path.join(DEST_DIRS[category], filename)
                        os.rename(src_path, dest_path)
                        break  # Stop checking patterns once matched

if __name__ == "__main__":
    extract_and_classify()












