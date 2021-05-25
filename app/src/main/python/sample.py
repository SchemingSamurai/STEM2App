import os
import io
import PIL.Image as Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
import math
import cv2 as cv
from matplotlib import pyplot as plt


from array import array


def areClose(color1, color2):
  return sum(abs(color1 - color2)) < 50

def areShades(color1, color2):
  imax = (list(color1)+list(color2)).index(max(list(color1)+list(color2))) % 3
  ratio = color1[imax] / color2[imax]
  sum = 0
  for i in range(3):
    if i != imax:
      sum += max([abs(color1[i] - color2[i] * ratio), abs(color1[i] / ratio - color2[i])])
  return sum < 40


def monotonicrow(i,j, m, n, avgimg):
  if j <= 1 or j >= n-2:
    return False
  shades = True
  for a in range(j-2,j+1):
    for b in range(a+1,j+2):
      if not areShades(avgimg[i][a], avgimg[i][b]):
        shades = False
  if not shades:
    return True
  for b in range(j-2, j+2):
    for k in range(3):
      if (avgimg[i][b+1][k] - avgimg[i][b][k]) * (avgimg[i][j+1][k] - avgimg[i][j][k]) < 0:
        return False
  return True

def monotoniccol(i,j, m, n, avgimg):
  if i <= 1 or i >= m-2:
    return False
  shades = True
  for a in range(i-2,i+1):
    for b in range(a+1,i+2):
      if not areShades(avgimg[a][j], avgimg[b][j]):
        shades = False
  if not shades:
    return True
  for a in range(i-2,i+2):
    for k in range(3):
      if (avgimg[a+1][j][k] - avgimg[a][j][k]) * (avgimg[i+1][j][k] - avgimg[i][j][k]) < 0:
        return False
  return True

def isColorChange(image):
  m = 20
  n = 15
  ylow = 4
  yhigh = 16
  ydiff = yhigh-ylow
  xlow = 5
  xhigh = 10
  xdiff = xhigh-xlow
  img = np.asarray(Image.open(io.BytesIO(bytearray(image))))
  avgimg = np.mean(np.mean(np.asarray([np.asarray([img[img.shape[0] // m * i: img.shape[0] // m * (i+1), img.shape[1] // n * j: img.shape[1] // n * (j+1)] for j in range(xlow, xhigh)]) for i in range(ylow, yhigh)]),axis = 2), axis = 2)
  change = False
  for i in range(yhigh-ylow-1):
    for j in range(xhigh-xlow-1):
      c1 = avgimg[i][j]
      c2 = avgimg[i+1][j]
      c3 = avgimg[i][j+1]
      if not areClose(c1,c2) and (not areShades(c1,c2) or monotoniccol(i,j, ydiff, xdiff, avgimg)):
        change = True
      if not areClose(c1,c3) and (not areShades(c1,c3) or monotonicrow(i,j, ydiff, xdiff, avgimg)):
        change = True
  return change
