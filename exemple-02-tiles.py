#!env python3
import tiledMap as tim
#import src.tiledMap.view.pygameView as timView
import src.tiledMap.view.cairoView as timView

def main():
    # Set-up an IHM
    ihm= timView.Frame()
    game= Scenario()

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

class Scenario :
    def __init__(self):
        self.tiles= [
            tim.Tile( [ (1, 2), (1.98, 5.9), (4.98, 4.9), (4, 0) ] ),
            tim.Tile( [ (2, 6), (4, 8), (5, 5) ] ),
            tim.Tile( [(7,1), (9,1), (9,3), (7,3)] ),
            tim.Tile( [(7,4), (9,5), (7,6)] ),
        ]
        self.tiles[1].setTags( [1, 0, 0] )
        #self.body= Body2( 7.5, 5.2, 2.2 )

    def process( self, frame ):
        frame.initBackground()
        frame.drawFrameGrid()
        for tile in self.tiles :
            frame.drawTile( tile )
        #frame.drawBody( self.body )

        return True

if __name__ == "__main__":
    main()

    