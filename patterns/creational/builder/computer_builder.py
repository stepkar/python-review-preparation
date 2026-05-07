from dataclasses import dataclass, field
from enum import StrEnum
import collections
from typing import Optional, Self


class CPUArch(StrEnum):
  ARM64='arm64'
  x86_64='x86_64'



@dataclass(frozen=True, slots=True)
class Computer:
  CPU: CPUArch = field(default=CPUArch.x86_64)
  RAM: int = field(default=8)
  SSD: int = field(default=1024)
  motherboard: Optional[str] = field(default=None)
  GPU: Optional[str]=field(default=None)

  def __post_init__(self):
    if self.SSD < 512:
      raise ValueError("There is no SSD with low capacity. Sorry try again.")
    if self.SSD % 128 != 0:
      raise ValueError("There is no SSD with such capacity. Sorry try again.")
    if self.motherboard is None:
      raise ValueError("There is no computers without motherboard. Choose one!")


  def __str__(self):
    parts=[]
    if self.CPU:
      parts.append(self.CPU)
    if self.RAM:
      parts.append(self.RAM)
    if self.SSD:
      parts.append(self.SSD)
    if self.motherboard:
      parts.append(self.motherboard)
    if self.GPU:
      parts.append(self.GPU)
    return f'Computer({", ".join(str(p) for p in parts)})'

class ComputerBuilder:
  def __init__(self):
    self.parts = {}

  def add_cpu(self, cpu: CPUArch) ->Self:
    self.parts['cpu']=cpu
    return self

  def add_gpu(self, gpu:str) ->Self:
    self.parts['gpu']= gpu
    return self

  def add_motherboard(self, mboard:str)->Self:
    self.parts['mboard']=mboard
    return self

  def add_ssd(self, ssd:int)->Self:
    self.parts['ssd']=ssd
    return self

  def add_ram(self, ram:int)->Self:
    self.parts['ram'] = ram
    return self


  def build(self):
    return Computer(
      CPU=self.parts.get('cpu', CPUArch.ARM64),
      GPU=self.parts.get('gpu', None),
      motherboard=self.parts.get('mboard',None),
      SSD= self.parts.get('ssd', 1024),
      RAM= self.parts.get('ram', 8)
    )

if __name__ == '__main__':
  builder=ComputerBuilder()
  computer = (builder.add_cpu(CPUArch.ARM64)
              .add_gpu("H200")
              # .add_motherboard("ASUS")
              .add_ssd(2048)
              .add_ram(64)
              .build())
  print(computer)


