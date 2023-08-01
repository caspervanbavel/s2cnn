## Installation

We are going to mostly use pip because conda seems to fail to solve the environment.
Since the lie_learn installation is broken, use my fork.

```bash
conda create --name cuda11 python=3.8.10
conda activate cuda11
pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
pip install cupy-cuda111
pip install pynvrtc==9.2
pip install git+https://github.com/caspervanbavel/lie_learn.git
```

You need to set the path to your local nvrtc (for cuda 11.1) using an environment variable:

`NVRTC_DLL="C:\ProgramData\Miniconda3\envs\cuda11\Lib\site-packages\torch\lib\nvrtc64_111_0.dll"`

On Windows, the DLL name is hardcoded into the library, and depends on the cuda version.
Change the following line in pynvrtc:

`C:\ProgramData\Miniconda3\envs\cuda11\Lib\site-packages\pynvrtc\interface.py`,
Line 96:
```python
    def_lib_name = 'nvrtc64_111_0.dll'
```

Now everything should work. Run the tests to check:
```bash
python -m tests.so3_fft
```

To install s2cnn locally, run:
```bash
python setup.py install
```
