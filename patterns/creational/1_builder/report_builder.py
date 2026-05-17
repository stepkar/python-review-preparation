from dataclasses import dataclass
from typing import Any, List, Dict


@dataclass
class Report:
  title: str
  data:List[Dict[str, Any]]
  filters: Dict[str, Any]
  output_format: str = 'json'