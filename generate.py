import config
from pathlib import Path

sys.path.append('stylegan2')

import dnnlib
import dnnlib.tflib as tflib
import numpy as np

def generate_images(model_path, dest_path, seed_range):
    sc = dnnlib.SubmitConfig()
    sc.num_gpus = 1
    sc.submit_target = dnnlib.SubmitTarget.LOCAL
    sc.local.do_not_copy_source_files = True
    sc.run_dir_root = './stylegan2/results'
    sc.run_desc = 'generate_images'

    dnnlib.submit_run(sc, 'run_generator.generate_images', network_pkl=model_path, seeds=range(seed_range), truncation_psi=1.0, dest=dest_path)

if len(sys.argv) == 3:
    for config_item in config.config:
        model_path = sys.argv[1] + '/{}.pkl'.format(config_item["model"])
        dest_path = sys.argv[2] + '/{}'.format(config_item["model"])
        seed_range = 1000
        Path(dest_path).mkdir(parents=True, exist_ok=True)
        generate_images(model_path, dest_path, seed_range)

else:
    print("Expected cmd line arg: path to models directory; path to imgs directory")
