"""
This is where the implementation of the plugin code goes.
The FlipTiles-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Set path for modules
sys.path.append('.')
from src.plugins.ValidTiles.ValidTiles import ValidTiles

# Setup a logger
logger = logging.getLogger('FlipTiles')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class FlipTiles(PluginBase):
    def main(self, pos, chains):
        active_node = self.active_node
        core = self.core
        META = self.META
        
        row = pos[0]
        col = pos[1]
        
        # Get the tile node referred to by pos
        gsNode = {"rootId": active_node.get("rootId"), "nodePath": core.get_pointer_path(active_node, "currentState")}
        gsName = core.get_attribute(gsNode, "name")
        curPlayerNode = {"rootId": gsNode.get("rootId"), "nodePath": core.get_pointer_path(gsNode, "currentPlayer")}
        color = core.get_attribute(curPlayerNode, "color")
        gsComps = core.get_children_paths(gsNode)
        for path in gsComps:
            boardNode = {"rootId": active_node.get("rootId"), "nodePath": path}
            if (core.is_instance_of(boardNode, META['Board'])):
                tiles = core.get_children_paths(boardNode)
                for tilePath in tiles:
                    tile = {"rootId": active_node.get("rootId"), "nodePath": tilePath}
                    if ((core.get_attribute(tile, "row") == row) and (core.get_attribute(tile, "column") == col)):
                        break
                break
        
        canPlace = core.get_attribute(tile, "isValid")
        
        # Place and flip pieces
        logger.info(canPlace)
        if canPlace:
            logger.info("A piece can be placed here at Tile (" + str(row) +", " + str(col) + ")")
            
            # New gamestate creation

            newGS = core.copy_node(gsNode, core.get_parent(gsNode))

            nameStart = gsName[:-1]
            try:
                num = int(gsName[-1])
                num = num + 1
                if num == 10:
                    try:
                        num2 = int(gsName[-2])
                        nameStart = gsName[:-2]
                        num = num2 * 10 + num
                    except:
                        pass
            except:
                nameStart = gsName
                num = 1
            newGSName = nameStart + str(num)
            logger.info(newGSName)

            core.set_attribute(newGS, "name", newGSName)
            logger.debug(core.get_attribute(newGS, "name"))

            gsChildren = core.load_sub_tree(newGS)
            for child in gsChildren:
                # Set the new currentPlayer
                if (core.is_instance_of(child, META['Player'])):
                    thisCol = core.get_attribute(child, "color")
                    #logger.error(thisCol)
                    if thisCol != color:
                        #newCurPlayerChar = core.get_path(child)[-1]
                        #logger.info(newCurPlayerChar)
                        core.set_pointer(newGS, "currentPlayer", child)
                        logger.error(child)
                        logger.warn("currentPlayer path: " + core.get_pointer_path(newGS, "currentPlayer"))
                    # Flip tiles that need to be flipped
                elif (core.is_instance_of(child, META['Piece'])):
                    pieceTile = core.get_parent(child)
                    for chain in chains:
                        if [core.get_attribute(pieceTile, "row"), core.get_attribute(pieceTile, "column")] in chain:
                            logger.info("row to flip: " + str(core.get_attribute(pieceTile, "row")) + ", column to flip: " + str(core.get_attribute(pieceTile, "column")))
                            logger.info("initial color: " + core.get_attribute(child, "color"))
                            core.set_attribute(child, "color", color)
                            logger.info("new color: " + core.get_attribute(child, "color"))
                            
                            # Update counts
                            whiteCount = core.get_attribute(newGS, "whiteCount")
                            blackCount = core.get_attribute(newGS, "blackCount")
                            if (color == "white"):
                                core.set_attribute(newGS, "whiteCount", whiteCount+1)
                                core.set_attribute(newGS, "blackCount", blackCount-1)
                            else:
                                core.set_attribute(newGS, "whiteCount", whiteCount-1)
                                core.set_attribute(newGS, "blackCount", blackCount+1)
            
            # Final update counts
            if (color == "white"):
                whiteCount = core.get_attribute(newGS, "whiteCount")
                core.set_attribute(newGS, "whiteCount", whiteCount+1)
            else:
                blackCount = core.get_attribute(newGS, "blackCount")
                core.set_attribute(newGS, "blackCount", blackCount+1)
            
            # Create new game state
            newGS_id = core.get_path(newGS)[-1]
            newGS_tile = tile
            newPath = tile["nodePath"]
            newPath = newPath[:3] + newGS_id + newPath[4:]
            newGS_tile["nodePath"] = newPath
            #logger.error(newGS_tile)

            # Create new piece on the correct tile
            newPiece = core.create_node({'parent': newGS_tile, 'base':META['Piece']})
            #logger.error(core.get_path(newPiece))
            core.set_attribute(newPiece, "color", color)

            # Set new currentMove
            #logger.warn(core.get_pointer_path(gsNode, "currentMove"))
            core.set_pointer(newGS, "currentMove", newPiece)
            #logger.warn(core.get_pointer_path(newGS, "currentMove"))
            
            # Set new currentState and previousState
            core.set_pointer(newGS, "previousState", gsNode)
            core.set_pointer(active_node, "currentState", newGS)
            
            ValidTiles.main(self)

            logger.debug(core.get_children_paths(newGS))
            self.util.save(self.root_node, self.commit_hash, self.branch_name, 'New GS created')
        else:
            logger.error("A piece cannot be placed here at Tile (" + str(row) +", " + str(col) + ")")