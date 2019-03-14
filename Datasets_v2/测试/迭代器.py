 -*- coding: utf-8 -*-
class MyNumbers:
  def __init__(self,num):
      self.num = num

  def __iter__(self):
    self.a = 1
    return self
 
  def __next__(self):
    if self.a <= self.num:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration
 
myclass = MyNumbers(10)
myiter = iter(myclass)
 
for x in myiter:
  print(x)

