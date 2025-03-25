# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Float2, Box
from src.tiledland import Shape, Body, Tile, Scene 

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Scene_init():
    scene= Scene()
    assert type(scene) == Scene
    assert scene.size() == 0
    assert scene.box() == Box()

def test_Scene_initLine():
    scene= Scene().initializeLine(3)
    assert scene.tile(1).id() == 1
    assert scene.tile(2).id() == 2
    assert scene.tile(3).id() == 3
    assert scene.tiles() == [ scene.tile(1), scene.tile(2), scene.tile(3) ]
    assert scene.edges() == []

    assert scene.tile(1).position().asTuple() == (0.0, 0.0)
    assert scene.tile(1).envelope() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

    assert scene.tile(2).position().asTuple() == (1.0, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in scene.tile(2).envelope() ]
    assert env == [(0.55, 0.45), (1.45, 0.45), (1.45, -0.45), (0.55, -0.45)]

    assert scene.tile(3).position().asTuple() == (2.0, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in scene.tile(3).envelope() ]
    assert env == [(1.55, 0.45), (2.45, 0.45), (2.45, -0.45), (1.55, -0.45)]
    
def test_Scene_construction():
    scene= Scene().initializeLine(3)
    assert scene.tile(1).adjacencies() == []
    assert scene.tile(2).adjacencies() == []
    assert scene.tile(3).adjacencies() == []
    scene.connect(1, 2)
    scene.connect(1, 3)
    scene.connect(2, 2)
    scene.connect(2, 1)
    scene.connect(3, 1)
    scene.connect(3, 2)
    scene.connect(3, 3)
    assert scene.tile(1).adjacencies() == [2, 3]
    assert scene.tile(2).adjacencies() == [1, 2]
    assert scene.tile(3).adjacencies() == [1, 2, 3]
    assert scene.edges() == [ (1, 2), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3) ]
    idScene= id(scene)
    scene.initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    print(f">>> {scene.edges()}")
    assert( idScene == id(scene) )
    assert scene.edges() == [ (1, 1), (1, 3), (2, 1), (2, 2), (3, 2) ]

def test_Scene_str():
    scene= Scene().initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    scene.tile(2).append( Body(1) )

    print( f">>> {scene}." )

    assert "\n"+str(scene)+"\n" == """
Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[1, 3] bodies(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[1, 2] bodies(1)
  - Body-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] bodies(0)
"""

def test_Scene_pod():
    scene= Scene().initializeLine(4)
    scene.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    scene.tile(1).position().set( 5.0, 3.0 )
    scene.tile(2).position().set( 5.0, 15.0 )
    scene.tile(3).position().set( 1.0, 9.0 )
    scene.tile(4).position().set( 9.0, 9.0 )

    print(f">>>\n{scene}")
    assert '\n'+ str(scene) +'\n' == """
Scene:
- Tile-1 ⌊(4.55, 2.55), (5.45, 3.45)⌉ adjs[2, 3, 4] bodies(0)
- Tile-2 ⌊(4.55, 14.55), (5.45, 15.45)⌉ adjs[1, 3, 4] bodies(0)
- Tile-3 ⌊(0.55, 8.55), (1.45, 9.45)⌉ adjs[1, 2] bodies(0)
- Tile-4 ⌊(8.55, 8.55), (9.45, 9.45)⌉ adjs[1, 2] bodies(0)
"""

def test_Scene_box():
    scene= Scene()
    assert scene.box() == Box( [Float2(0.0, 0.0)] )

    scene= Scene().initializeLine(4)
    print( scene.box() )
    assert scene.box().asZip() == [(-0.45, -0.45), (3.45, 0.45)]
    
    scene.initializeGrid( [[0, 1], [0, -1]] )
    print( scene.box() )
    assert scene.box().asZip() == [(-0.5, -0.5), (1.6, 1.6)]

def test_Scene_podable():
    scene= Scene().initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    pod= scene.asPod()

    assert pod.numberOfWords() == 1
    assert pod.words() == ["Scene"]
    assert pod.word() == "Scene"

    assert pod.numberOfIntegers() == 0
    assert pod.integers() == []
    
    assert pod.numberOfValues() == 0
    assert pod.values() == []
    
    assert pod.numberOfChildren() == 3
    assert pod.children() == [ t.asPod() for t in scene.tiles() ]

def test_Scene_podcopy():
    scene= Scene().initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    assert scene.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

    assert '\n'+ str(scene) +'\n' == """
Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[1, 3] bodies(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[1, 2] bodies(0)
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] bodies(0)
"""

    print("Go for the copying...")
    sceneBis= scene.podCopy()
    scene.connect(3, 1)

    assert type(scene) == type(sceneBis)
    assert sceneBis.size() == 3

    print(f">>>\n{sceneBis}")
    assert '\n'+ str(sceneBis) +'\n' == """
Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[1, 3] bodies(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[1, 2] bodies(0)
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] bodies(0)
"""

    assert sceneBis.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

def test_Scene_connection():
    scene= Scene().initializeLine( 3, connect=False )
    scene.connect(1, 2)
    scene.connect(2, 2)
    scene.connect(2, 3)
    scene.connect(3, 2)
    print( f"---\n{scene}.")
    assert str(scene) == """Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[2] bodies(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[2, 3] bodies(0)
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] bodies(0)"""

    assert scene.tile(1).adjacencies() == [2]
    assert scene.tile(2).adjacencies() == [2, 3]
    assert scene.tile(3).adjacencies() == [2]
    
    assert scene.isEdge(1, 2)
    assert scene.isEdge(2, 2)
    assert scene.isEdge(3, 2)
    assert not scene.isEdge(2, 1)
    assert not scene.isEdge(1, 3)
    assert not scene.isEdge(3, 1)
  
def test_Scene_withBodies():
    scene= Scene().initializeGrid( [[0, 1],[-1, 0]] )
    
    assert scene.testNumberOfBodies() == 0
    assert scene.tile(1).count() == 0
    assert scene.tile(2).count() == 0
    assert scene.tile(3).count() == 0
    
    scene.popBodyOn(2)

    assert scene.testNumberOfBodies() == 1
    assert scene.tile(1).count() == 0
    assert scene.tile(2).count() == 1
    assert scene.tile(3).count() == 0

    scene.popBodyOn(1)

    assert scene.testNumberOfBodies() == 2
    assert scene.tile(1).count() == 1
    assert scene.tile(2).count() == 1
    assert scene.tile(3).count() == 0

    bod= scene.popBodyOn(2)
    bod.setId(4)

    assert scene.testNumberOfBodies() == 3
    assert scene.tile(1).count() == 1
    assert scene.tile(2).count() == 2
    assert scene.tile(3).count() == 0

    print( f"---\n{scene}.")
    assert str(scene) == """Scene:
- Tile-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[1, 2] bodies(1)
  - Body-2 ⌊(-0.5, 0.6), (0.5, 1.6)⌉
- Tile-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 2, 3] bodies(2)
  - Body-1 ⌊(0.6, 0.6), (1.6, 1.6)⌉
  - Body-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉
- Tile-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2, 3] bodies(0)"""

    scene.clearBodies()

    assert scene.testNumberOfBodies() == 0
    assert scene.tile(1).count() == 0
    assert scene.tile(2).count() == 0
    assert scene.tile(3).count() == 0