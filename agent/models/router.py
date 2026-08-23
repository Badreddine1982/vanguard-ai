from typing import Tuple

import torch
import torch.nn as nn
import torch.optim as optim


class AdaptiveRouter(nn.Module):
    """موجه عصبي ذاتي التعلم"""

    def __init__(self, input_dim: int, output_dim: int = 3):
        super().__init__()

        self.input_dim = input_dim
        self.output_dim = output_dim

        self.net = self._build_net(input_dim, output_dim)

        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.loss_fn = nn.CrossEntropyLoss()
        self.training_count = 0

    @staticmethod
    def _build_net(input_dim: int, output_dim: int) -> nn.Sequential:
        return nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim),
            nn.Softmax(dim=-1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """المرور الأمامي"""
        return self.net(x)

    def predict(self, features: torch.Tensor) -> Tuple[int, float]:
        """التنبؤ بقرار"""
        self.eval()
        with torch.no_grad():
            probs = self.forward(features)
            idx = int(torch.argmax(probs, dim=1).item())
            confidence = float(probs[0][idx].item())
            return idx, confidence

    def train_step(self, features: torch.Tensor, target: int) -> float:
        """خطوة تدريب واحدة"""
        self.train()
        self.optimizer.zero_grad()

        output = self.forward(features)
        loss = self.loss_fn(output, torch.tensor([target], device=features.device))

        loss.backward()
        self.optimizer.step()

        self.training_count += 1
        return float(loss.item())

    def get_weights(self) -> dict:
        """استخراج الأوزان للحفظ"""
        return self.state_dict()

    def set_weights(self, weights: dict):
        """تحميل الأوزان من الذاكرة"""
        self.load_state_dict(weights)

    def expand_input(self, new_dim: int):
        """توسيع الشبكة لإضافة ميزات جديدة"""
        if new_dim <= self.input_dim:
            return

        old_weights = self.net[0].weight.data

        new_net = self._build_net(new_dim, self.output_dim)

        new_weights = new_net[0].weight.data
        new_weights[:, : self.input_dim] = old_weights
        new_net[0].weight.data = new_weights

        self.net = new_net
        self.input_dim = new_dim

        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
