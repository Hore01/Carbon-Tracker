import json
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class FactorSet:
data: Dict[str, Any]


@staticmethod
def from_json_str(s: str) -> "FactorSet":
return FactorSet(json.loads(s))


@staticmethod
def from_file(path: str) -> "FactorSet":
with open(path, "r", encoding="utf-8") as f:
return FactorSet(json.load(f))


def get(self, *keys, default=None):
node = self.data
for k in keys:
if not isinstance(node, dict) or k not in node:
return default
node = node[k]
return node