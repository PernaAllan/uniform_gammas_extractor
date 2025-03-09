#Não ta dando certo

import os
import re
import tarfile

tgz_path = "/lustre06/project/6084498/dnn/data/all_gammas.tgz"
base_dir = "/lustre06/project/6084498/dnn/data/" #this is the common output directory

categories = {
    "uniform_gammas_base_group": re.compile(r'^uniform_gammas/uniform_gammas_100k_group\d+\.hdf5$'),
    "uniform_gammas_base_group_FVGains": re.compile(r'^uniform_gammas/uniform_gammas_100k_group\d+_fvgains\.rpk\.hdf5$'),
    "uniform_gammas_noel": re.compile(r'^uniform_gammas/uniform_gammas_noel_100k_group\d+\.hdf5$'),
    "uniform_gammas_noel_FVGains": re.compile(r'^uniform_gammas/uniform_gammas_noel_100k_group\d+_fvgains\.rpk\.hdf5$')
}

#Creating output directories
for dir_name in categories:
    os.makedirs(os.path.join(base_dir, dir_name), exist_ok=True)

with tarfile.open(tgz_path, "r:gz") as tar:
    for member in tar:
        if not member.isfile() or not member.name.startwith('uniform_gammas/'):
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
                break

