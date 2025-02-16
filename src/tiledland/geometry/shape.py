import math
from ..pod import Podable, Pod
from .float2 import Float2
from .box import Box

class Shape(Podable):

    # Constructor/Destructor:
    def __init__( self, size= 1.0 ):
        self.initializeSquare( size )

    # Initialization:
    def initializeSquare(self, size):
        demi= size*0.5
        self._points= [
            Float2( -demi, +demi ),
            Float2( +demi, +demi ),
            Float2( +demi, -demi ),
            Float2( -demi, -demi )
        ]
        return self

    def initializeRegular(self, size, numberOfVertex= 6):
        radius= size*0.5
        self._points= []
        delta= math.pi/(numberOfVertex/2)
        angle= math.pi  - delta/2
        delta= math.pi/(numberOfVertex/2)
        for i in range(numberOfVertex) :
            p= Float2( math.cos(angle)*radius, math.sin(angle)*radius)
            self._points.append(p)
            angle+= -delta
        return self

    # Accessor:
    def points(self):
        return self._points
    
    def box(self):
        return Box(self.points())
    
    def envelope(self):
        return [ (p.x(), p.y()) for p in self._points ]

    # Construction:
    def setEnveloppe( self, envelopes ):
        self._points= [ Float2(x, y) for x, y in envelopes ]
        return self
    
    def round(self, precision):
        for p in self._points :
            p.round(precision)
    
    # Transform:
    def asList(self):
        l= []
        for p in self._points:
            l+= [p.x(), p.y()]
        return l
    
    # Object operator:
    def copy(self):
        cpy= type(self)()
        cpy._points= [ p.copy() for p in self.points() ]
        return cpy

    # to str
    def str(self, typeName="Shape"): 
        # Myself :
        s= f"{typeName} {len(self._points)}" 
        s+= str( [(round(x, 2), round(y, 2)) for x, y in self.box().asZip()] )
        return s
    
    def __str__(self): 
        return self.str()
    
    # Pod interface:
    def asPod(self):
        return Pod().fromLists( ["Shape"], [], self.asList(), [] )
    
    def fromPod( self, aPod ):
        values= aPod.values()
        self._points= [
            Float2(x, y)
            for x, y in zip( values[::2], values[1::2] )
        ]
        return self
