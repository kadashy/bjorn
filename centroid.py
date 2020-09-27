import numpy as np

class Centroid:

    def __init__(self,points):
        self.points = points

    def get_centroide(self):
        # point = (self.points)
        # average = sum(orders) / len(orders)
        # print (point)
        points_array = np.array(self.points)
        # point = self.points.split(",")
        index = 0
        point = {}
        xsum = 0
        ysum = 0

        for input in self.points:
            length = (len(self.points))
            splited = input.split(",")
            index = index + 1
            # print (index)
            xsum = xsum + float(splited[0])
            ysum = ysum + float(splited[1])
            point[splited[2]] = [[xsum],[ysum]]

        print(point)

        # ml = []
        # keys = point.keys()
        # a = 0
        # for key in point:
        #     # value = list(map(float, point[key][0]))
        #     # print (value)
        #     a = map(float,point[key][0])
        #     print (key)
        #     print (a[0])
        #
        #     avr = value/length
        #     print (avr)
        #     # point[key][0] = value/length
            # point[key][1] = point[key][1] / len(self.points)

        # yavr = ysum / len(self.points)
        # xavr = xsum / len(self.points)
        # print (len(self.points))
        # print (point)

            # point[splited[2]] = [index,splited[0],splited[1]]
            # index = index + 1
        #     point[point_split[2]] = {point_split[0],point_split[1]}
            # print (point[index])
            # points_array[int(any)] = (self.points[int(any)]).split(",")
            # print (points_array[any])
            # for x in list:
            #     print(x)

        #
        # for point in
        # print (n[1])


    # #        for point in points:
    # #            print(point)
    # #            x = int(point[0][0])
    # #            print("asd: " + x)



    #         centroid = (sum(x) / len(points), sum(y) / len(points))
    #         print(centroid)
    #         return centroid
