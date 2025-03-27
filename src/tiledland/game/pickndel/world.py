
from .robot import Robot
from ... import Float2, Shape, Box, scene, Tile, artist
import random

class Mission:
    def __init__( self, start, final, reward, owner ):
        self.start= start
        self.final= final
        self.reward= reward
        self.owner= owner

    def asList(self):
        return [self.start, self.final, self.reward, self.owner]
    
    def asTuple(self):
        return self.start, self.final, self.reward, self.owner

class World( scene.Scene ):
    def __init__(self, numberOfPlayers= 1):
        super().__init__(Robot)
        self._missions= []
        # Initialize Artist :
        self._artist= artist.Artist().initializePNG( "shot-pickndel.png" )
        self._artist.flip()
        self._artist.fitBox( Box([Float2(-0.5, -0.5), Float2(9.5, 6.5)] ), 10 )
        #self._artist.fitBox( self.box(), 10 )
        self.marketBrush= self._artist._panel[6]
        self.marketBrush.width= 8

    # Accessor: 
    def missions(self):
        return self._missions

    def isMission(self, iMission):
        return ( 0 < iMission and iMission <= len(self._missions) )

    def mission(self, index):
        return self._missions[index-1]
    
    def missionIndexes(self):
        l= []
        i= 1
        for m in self._missions :
            if m.start > 0 :
                l.append(i)
            i+= 1
        return l
    
    def mobileTiles(self, iPlayer):
        return [ m.tile() for m in self.agents(iPlayer) ]
    
    # Construction:
    def initializeMoves(self):
        for group in range( self.numberOfGroups() ) :
            for mobile in self.agents(group) :
                mobile.setMove(0)
    
    # Mission :
    def setMissions( self, aListOfTuples, pay= 10 ):
        self._missions= [
            Mission(iFrom, iTo, pay, 0)
            for iFrom, iTo in aListOfTuples 
        ]
    
    def clearMissions(self):
        self._missions= []
        for group in range(self.numberOfGroups()+1) :
            for iRobot in range(1, self.numberOfAgents(group)+1) :
                self.agent( iRobot, group ).setMission(0)
        return self

    def addMission( self, iFrom, iTo, pay= 10 ):
        self._missions.append( Mission(iFrom, iTo, pay, 0) )
        return len(self._missions)
    
    def addMissionAtRandom( self ):
        tileIndexes= range( 1, self.size()+1 )
        return self.addMission( random.choice( tileIndexes ), random.choice(tileIndexes), 10 )

    def updateMission(self, iMission, iFrom, iTo, pay, owner):
        self._missions[iMission-1]= Mission(iFrom, iTo, pay, owner)

    def addRandomMission(self):
        bound= self._engine._map.size()+1
        iFrom= random.randrange(1, bound)
        iTo= random.randrange(1, bound)
        pay= 10+random.randrange(bound)
        self._engine.addMission( iFrom, iTo, pay )
        return iFrom, iTo, pay

    # Moving:
    def move(self, iFrom, clockDir):
        if self.tile(iFrom).count() > 0 and clockDir == 0 :
            return iFrom
        iTo= self.clockposition( iFrom, clockDir ) 
        return self.teleport(iFrom, iTo)

    def teleport( self, iFrom, iTo ):
        if self.tile(iFrom).count() == 0 or self.tile(iTo).count() :
            return False
        # move:
        # Get from iFrom
        robot= self.tile(iFrom).agent()
        self.tile(iFrom).clear()

        # Set on iTo
        self.tile(iTo).append(robot)
        robot.setTile( iTo )
        robot.setPosition( self.tile(iTo).position() )
        return iTo
    
    def tileFromPod(self, aPod):
        tile= Tile()
        flags= aPod.flags()
        tile._num= flags[0]
        tile._matter= flags[1]
        tile._adjacencies= flags[2:]
        # Convert Values:
        vals= aPod.values()
        xs= [ vals[i] for i in range( 0, len(vals), 2 ) ]
        ys= [ vals[i] for i in range( 1, len(vals), 2 ) ]
        tile._center= Float2( xs[0], ys[0] )
        tile._points= [ Float2(x, y) for x, y in zip(xs[1:], ys[1:]) ]
        # Load pices:
        tile._pieces= [ Robot().fromPod(p) for p in aPod.children() ]
        tile._piecesBrushId = [ 10+mob.owner() for mob in tile._pieces ]
        tile._piecesShapeId = [ 0 for mob in tile._pieces ]
        return tile

    def fromPod(self, aPod):
        self._tiles= [None]
        self._shapes= []
        self._size= 0
        kids= aPod.children()
        for kid in kids :
            if kid.family() == "Shape" :
                self.addShape( Shape().fromPod( kid ) )
            if kid.family() == "Tile" :
                self.addTile( self.tileFromPod( kid ) )
        # Update cros knoldge:
        for t in range( 1, self.size()+1 ):
            for p in range( len( self.tile(t)._pieces ) ) :
                iPlayer= self.tile(t)._pieces[p].flag(1)
                iRobot= self.tile(t)._pieces[p].flag(2)
                self._mobiles[iPlayer][iRobot-1]= t
        return self
    
    # Rendering :
    def render(self):
        self._artist.drawScene( self )
        # Market:
        self._artist.drawPolygon(
            [6.55, 6.55, 9.5, 9.5], [2.45, -0.6, -0.6, 2.45],
            self.marketBrush
        )
        self._artist._fontSize= 20
        self._artist.write( 6.6, 2.2, "Market Place:", self.marketBrush )
        self._artist._fontSize= 16
        sep= 0.0
        for i in self.missionIndexes() :
            mFrom, mTo, pay, iPlayer= self.mission(i).asTuple()
            self._artist.write( 6.8, 1.9-sep, f".{i}", self.marketBrush) 
            self._artist.write( 7.2, 1.9-sep, f"- {mFrom} to: {mTo}", self.marketBrush )
            if iPlayer == 0 :
                self._artist.write( 8.5, 1.9-sep, f"({pay} ¢)", self.marketBrush )
            else :
                self._artist.write( 8.4, 1.9-sep, f"(Team-{iPlayer})", self.marketBrush )
            sep+= 0.24
        # Finalize:
        self._artist.flip()

