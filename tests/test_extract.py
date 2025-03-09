import tarfile
import re

# Paths
TGZ_FILE = "/lustre06/project/6084498/dnn/data/all_gammas.tgz"

# Patterns to classify files
PATTERNS = {
    "base": re.compile(r"uniform_gammas_100k_group\d+\.hdf5$"),
    "noel": re.compile(r"uniform_gammas_noel_100k_group\d+\.hdf5$"),
    "fvgains": re.compile(r"uniform_gammas_100k_group\d+_fvgains\.rpk\.hdf5$"),
    "noel_fvgains": re.compile(r"uniform_gammas_noel_100k_group\d+_fvgains\.rpk\.hdf5$")
}

def test_extraction():
    """Check which files match the expected patterns without extracting."""
    with tarfile.open(TGZ_FILE, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.startswith("uniform_gammas/"):
                filename = member.name.split("/")[-1]  # Extract filename only
                
                for category, pattern in PATTERNS.items():
                    if pattern.match(filename):
                        print(f"MATCH: {filename} -> {category}")
                        break  # Stop checking once matched
                else:
                    print(f"NO MATCH: {filename}")

if __name__ == "__main__":
    test_extraction()
