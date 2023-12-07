"""
This is where the implementation of the plugin code goes.
The ValidTiles-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('ValidTiles')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ValidTiles(PluginBase):
    def main(self):
        active_node = self.active_node
        core = self.core
        META = self.META

        gsNode = {"rootId": active_node.get("rootId"), "nodePath": core.get_pointer_path(active_node, "currentState")}
        
        curPlayerNode = {"rootId": active_node.get("rootId"), "nodePath": core.get_pointer_path(gsNode, "currentPlayer")}
        color = core.get_attribute(curPlayerNode, "color")
        canPlace = False  
        diffCols = []
        sameCols = []
        flips = {}
        
        
        gsComps = core.get_children_paths(gsNode)
        for path in gsComps:
            boardNode = {"rootId": active_node.get("rootId"), "nodePath": path}
            if (core.is_instance_of(boardNode, META['Board'])):
                tiles = core.get_children_paths(boardNode)
                # Find all pieces on the board
                for tilePath in tiles:
                    tile = {"rootId": active_node.get("rootId"), "nodePath": tilePath}
                    rowNum = core.get_attribute(tile, "row")
                    colNum = core.get_attribute(tile, "column")
                    cPaths = core.get_children_paths(tile)
                    if (len(cPaths) != 0):
                        childColorNode = {"rootId": tile.get("rootId"), "nodePath": cPaths[0]}
                        tileColor = core.get_attribute(childColorNode, "color")
                        if (tileColor != color):
                            diffCols.append([rowNum, colNum])
                        else:
                            sameCols.append([rowNum, colNum])
                # Find valid tiles
                for tilePath in tiles:
                    tile = {"rootId": active_node.get("rootId"), "nodePath": tilePath}
                    row = core.get_attribute(tile, "row")
                    col = core.get_attribute(tile, "column")
                    chains = []
                    if ([row, col] not in diffCols and [row, col] not in sameCols):
                        for y in [-1, 0, 1]:
                            for x in [-1, 0, 1]:
                                curChain = []
                                if (y == 0 and x == 0):
                                    continue
                                ydiff = y
                                xdiff = x
                                if ([row + y, col + x] in diffCols):
                                    while [row + ydiff, col + xdiff] in diffCols:
                                        curChain.append([row + ydiff, col + xdiff])
                                        ydiff = ydiff + y
                                        xdiff = xdiff + x
                                    if ([row + ydiff, col + xdiff] in sameCols):
                                        chains.append(curChain)
                        if (len(chains) > 0):
                            #logger.info(tilePath)
                            pos = str(row) + " " + str(col)
                            flips[pos] = chains
                            core.set_attribute(tile, "isValid", True)
                        else:
                            core.set_attribute(tile, "isValid", False)
                    else:
                        core.set_attribute(tile, "isValid", False)
                
                logger.debug(flips)

        return flips
