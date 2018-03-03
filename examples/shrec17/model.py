# pylint: disable=E1101,R,C
import torch.nn as nn
import torch.nn.functional as F

from s2cnn.ops.s2_localft import equatorial_grid as s2_equatorial_grid
from s2cnn.nn.soft.s2_conv import S2Convolution
from s2cnn.ops.so3_localft import equatorial_grid as so3_equatorial_grid
from s2cnn.nn.soft.so3_conv import SO3Convolution

class Model(nn.Module):
    def __init__(self, nclasses):
        super().__init__()

        self.features = [6,  20, 60, 100, nclasses]
        self.bandwidths = [64, 20, 10, 7]

        assert len(self.bandwidths) == len(self.features) - 1

        sequence = []

        # S2 layer
        grid = s2_equatorial_grid(max_beta=0, n_alpha=2 * self.bandwidths[0], n_beta=1)
        sequence.append(S2Convolution(self.features[0], self.features[1], self.bandwidths[0], self.bandwidths[1], grid))

        # SO3 layers
        for l in range(1, len(self.features) - 2):
            nfeature_in = self.features[l]
            nfeature_out = self.features[l + 1]
            b_in = self.bandwidths[l]
            b_out = self.bandwidths[l + 1]

            sequence.append(nn.BatchNorm3d(nfeature_in, affine=True))
            sequence.append(nn.ReLU())
            grid = so3_equatorial_grid(max_beta=0, max_gamma=0, n_alpha=2 * b_in, n_beta=1, n_gamma=1)
            sequence.append(SO3Convolution(nfeature_in, nfeature_out, b_in, b_out, grid))

        sequence.append(nn.BatchNorm3d(self.features[-2], affine=True))
        sequence.append(nn.ReLU())

        self.sequential = nn.Sequential(*sequence)

        # Output layer
        output_features = self.features[-2]
        self.bn_out2 = nn.BatchNorm1d(output_features, affine=False)
        self.out_layer = nn.Linear(output_features, self.features[-1])

    def forward(self, x):  # pylint: disable=W0221
        x = self.sequential(x)  # [batch, feature, beta, alpha, gamma]
        x = x.view(x.size(0), x.size(1), -1).max(-1)[0]  # [batch, feature]

        x = self.bn_out2(x.contiguous())
        x = self.out_layer(x)
        return F.log_softmax(x, dim=1)