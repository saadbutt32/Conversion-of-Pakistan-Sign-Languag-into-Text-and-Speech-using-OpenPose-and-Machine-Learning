

def scalePoints(handRight,distance):
   
    ref = 50
    
    handRightResults = []
    handRightPoints = []
    handRightX = []
    handRightY = []
#    handRightC = []
#    threshold = 0
    for x in range(0,len(handRight),2): 
        handRightX.append(handRight[x])
    for x in range(1,len(handRight),2): 
        handRightY.append(handRight[x])
#    for x in range(2,len(handRight),3): 
#        handRightC.append(handRight[x]) 
    
    scale = ref/distance
    #print(scale)  
    
    for x in range(len(handRightX)):
        handRightX[x] *=scale
            
    for x in range(len(handRightY)):
        handRightY[x] *=scale
            
    
    for x in range(len(handRightY)):
        handRightX[x] *=2
        handRightY[x] *=2
    
            
    # storing computed keypoints
    for x in range(len(handRightX)): 
        #if handRightC[x] > threshold:
            handRightPoints.append((int(handRightX[x]) , int(handRightY[x]))) 
            handRightResults.append(handRightX[x])
            handRightResults.append(handRightY[x])
#        else:
#            handRightResults.append(None) 
            
    return handRightResults,handRightPoints