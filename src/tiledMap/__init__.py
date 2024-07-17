import math
from . import tile, joint

# Tiled Map Components:
Tile= tile.Tile
Joint= joint.Joint
#Map= map.Map
#Body2= body.Body2

# Point tool box:

def roundPoint( aPoint, precision=1 ):
    x, y= aPoint
    return (
        round( x, precision ),
        round( y, precision )
    )

# Point list generators:

def generatePointlist_circumscribe( center, nbFaces=4, diagonal=1.0):
    x, y= center
    points= []
    angle= math.pi - ((nbFaces-1)*math.pi/nbFaces)
    delta= math.pi/(nbFaces/2)
    for i in range(nbFaces) :
        points.append( (
            x+math.cos(angle)*diagonal,
            y+math.sin(angle)*diagonal
        ) )
        angle+= delta
    return points
