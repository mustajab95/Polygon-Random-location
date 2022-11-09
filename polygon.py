
import numpy as np
import random
from shapely.geometry import Polygon, Point

from google.colab import auth
auth.authenticate_user()
import pandas as pd
import re
import gspread
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)

sheetUrl = input("Enter the URL of the Source Sheet: ")

wb = gc.open_by_url(sheetUrl)
ws = wb.worksheet("Polygon")
rows_sheet = ws.get_all_records()
num_points=int(ws.acell("C3").value)
num_decimal=int(ws.acell("D3").value)

polygon_cell=[]
for i in range(3,8):
  latitude,longitude=ws.acell("B{}".format(i)).value.split(",")
  polygon_cell.append((round(float(latitude),num_decimal),round(float(longitude),num_decimal)))
print(polygon_cell)

# poly = Polygon([(37.75850848099701, -122.50833008408812), (37.75911919711413, -122.49648544907835),(37.751620611284935, -122.4937388670471),(37.74863453749236, -122.50742886185911)])
poly=Polygon(polygon_cell)

def polygon_random_points (poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds
    points = []
    while len(points) < num_points:
            random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
            if (random_point.within(poly)):
                points.append(random_point)
    return points

points = polygon_random_points(poly,num_points)
# Printing the results.
loop=3
for p in points:
    print(p.x,",",p.y)
    cell_val="A{}".format(loop)
    cell_data=str(p.x)+","+str(p.y)
    ws.update(cell_val,cell_data)
    loop+=1