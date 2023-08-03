# Installation
## Pytorch 1.8 with CUDA 11.1

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
*NOTE: I am not sure if this is actually necessary.*

`NVRTC_DLL="C:\ProgramData\Miniconda3\envs\cuda11\Lib\site-packages\torch\lib\nvrtc64_111_0.dll"`

On Windows, the DLL name is hardcoded into the library, and depends on the cuda version.
Change the following line in pynvrtc:

`C:\ProgramData\Miniconda3\envs\cuda11\Lib\site-packages\pynvrtc\interface.py`,
Line 96:
```python
    def_lib_name = 'nvrtc64_111_0.dll'
```

## Pytorch 2.0 with CUDA 11.7
```bash
conda create --name pytorch python=3.8.10
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
pip install cupy-cuda11x
pip install nvidia-cuda-nvrtc-cu11==11.7.99s
pip install pynvrtc==9.2
pip install pip install --no-use-pep517 git+https://github.com/caspervanbavel/lie_learn.git
```

You have to do the same patching here with pynvrtc. 
However this time, for some reason the dll is called `nvrtc64_112_0.dll` (despite being version 11.7) and was located in

`C:\ProgramData\Miniconda3\envs\pytorch\Lib\site-packages\nvidia\cuda_nvrtc\bin`.

## Testing

Now everything should work. Cd to `s2cnn` and run the tests to check:
```bash
python -m tests.so3_fft
```

If this  runs without raising an exception you are all good.

Finally, to install s2cnn locally, run:
```bash
python setup.py install
```

## Running example

Running the MNSIT example with non-rotated train and rotated test set:

```bash
cd examples/mnist
python gendata.py --no_rotate_train
python run.py
```

This example is small enough to run on a laptop. After about 30 minutes I get a test  accuracy of about 95%.

