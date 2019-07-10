


def isolatePoints(handRight):
    handRightResults = []
    handRightPoints = []
    handRightX = []
    handRightY = []
    
    for x in range(0,len(handRight),2): 
        handRightX.append(handRight[x])
    for x in range(1,len(handRight),2): 
        handRightY.append(handRight[x])
       
    
    # isolating keypoints 
    minX = min(handRightX , key=float)
    minX -= 10 
    for x in range(len(handRightX)):
        handRightX[x] -= minX
    
    minY = min(handRightY , key=float)
    minY -= 10 
    for x in range(len(handRightY)):
        handRightY[x] -= minY
        
    # storing computed keypoints
    for x in range(len(handRightX)): 
        handRightPoints.append((int(handRightX[x]) , int(handRightY[x]))) 
        handRightResults.append(handRightX[x])
        handRightResults.append(handRightY[x])

    return handRightResults,handRightPoints



def centerPoints(handRight):
    
    refX = 150
    refY=150
    
    handRightResults = []
    handRightPoints = []
    handRightX = []
    handRightY = []
    
    for x in range(0,len(handRight),2): 
        handRightX.append(handRight[x])
    for x in range(1,len(handRight),2): 
        handRightY.append(handRight[x])  
        
    p1 = [handRightX[0], handRightY[0]]
    p2 = [refX, refY]
    distanceX = p1[0]-p2[0]
    distanceY = p1[1]-p2[1]
    
    for x in range(len(handRightX)):
        handRightX[x] -= distanceX
     
    for x in range(len(handRightY)):
        handRightY[x] -= distanceY
    
    # storing computed keypoints
    for x in range(len(handRightX)): 
        handRightPoints.append((int(handRightX[x]) , int(handRightY[x]))) 
        handRightResults.append(handRightX[x])
        handRightResults.append(handRightY[x])

    return handRightResults,handRightPoints


"""
used for plotting skeleton
center to 300x 300y 
"""
def dummy_centerPoints(handRight):
    
    refX = 600
    refY=600
    
    handRightResults = []
    handRightPoints = []
    handRightX = []
    handRightY = []
    
    for x in range(0,len(handRight),2): 
        handRightX.append(handRight[x])
    for x in range(1,len(handRight),2): 
        handRightY.append(handRight[x])  
    
#    print(handRightX[0],handRightY[0])
    p1 = [handRightX[0], handRightY[0]]
    p2 = [refX, refY]
    distanceX = p1[0]-p2[0]
    distanceY = p1[1]-p2[1]
    
    for x in range(len(handRightX)):
        handRightX[x] -= distanceX
     
    for x in range(len(handRightY)):
        handRightY[x] -= distanceY
    


    for x in range(len(handRightX)): 
        handRightPoints.append((int(handRightX[x]) , int(handRightY[x]))) 
        handRightResults.append(handRightX[x])
        handRightResults.append(handRightY[x])

    return handRightResults,handRightPoints








