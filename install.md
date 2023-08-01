## Installation

We are going to mostly use pip because conda seems to fail to solve the environment.
Since the lie_learn installation is broken, use my fork.

```bash
conda create --name cuda11 python=3.8.10
conda activate cuda11
pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
pip install git+https://github.com/caspervanbavel/lie_learn.git
python setup.py install

# now test
python tests/so3_fft.py
```
