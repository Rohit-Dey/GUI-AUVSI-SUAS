import makePath, inputs

def textFile(a,b,c=1):
    f1 = open(b,"a")
    f1.write(str(a[0])+" "+str(a[1])+" "+str(c)+"\n")

    f1.close

for i in makePath.Waypoints:
    a=(i[0],i[1])
    wayptsAddition = textFile(a,"/home/jha02kanishk/Cells.txt",1)

for j in inputs.Obstacles:
    b=(j[0],j[1])
    obstacleAddition = textFile(j,"/home/jha02kanishk/Cells.txt",j[2])
    
for k in inputs.Waypoints:
    c=(k[0],k[1])
    waypointsAddition = textFile(k,"/home/jha02kanishk/Cells.txt",2)