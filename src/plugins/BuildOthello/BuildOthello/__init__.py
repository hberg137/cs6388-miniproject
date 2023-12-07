"""
This is where the implementation of the plugin code goes.
The BuildOthello-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
import json
from webgme_bindings import PluginBase

# Set path for modules
sys.path.append('.')
from src.plugins.ValidTiles.ValidTiles import ValidTiles

# Setup a logger
logger = logging.getLogger('BuildOthello')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class BuildOthello(PluginBase):
    def main(self):
        active_node = self.active_node
        core = self.core
        self.namespace = None
        META = self.META
        logger.debug('path: {0}'.format(core.get_path(active_node)))
        logger.info('name: {0}'.format(core.get_attribute(active_node, 'name')))
        logger.warn('pos : {0}'.format(core.get_registry(active_node, 'position')))
        logger.error('guid: {0}'.format(core.get_guid(active_node)))
        
        # Set currentState to starting state if null
        if (core.get_pointer_path(active_node, "currentState") == None):
            nodesList = core.load_sub_tree(active_node)
            nodes = {}
            for node in nodesList:
                # Go into each GameState node
                if (core.is_instance_of(node, META['GameState'])):
                    if (core.get_attribute(node, "name") == "OthelloGameState"):
                        core.set_pointer(active_node, "currentState", node)
                        self.util.save(self.root_node, self.commit_hash, self.branch_name, 'Set initial GS')
        
        gsNode = {"rootId": active_node.get("rootId"), "nodePath": core.get_pointer_path(active_node, "currentState")}
        flips = ValidTiles.main(self)
        
        ## OBJECT
        
        gameObj = []
        
        currentGS = {}
        currentGS["name"] = core.get_attribute(gsNode, "name")
        logger.info(core.get_attribute(gsNode, "name"))
        
        # Get child player node that currentPlayer points to
        curPlayerNode = {"rootId": gsNode.get("rootId"), "nodePath": core.get_pointer_path(gsNode, "currentPlayer")}
        currentGS["currentPlayer"] = core.get_attribute(curPlayerNode, "color")
        
        # Get child piece node that currentMove points to and the associated parent Tile node
        curMoveNode = {"rootId": gsNode.get("rootId"), "nodePath": core.get_pointer_path(gsNode, "currentMove")}
        if (curMoveNode["nodePath"] == None):
            childNode = {"rootId": gsNode.get("rootId"), "nodePath": str(core.get_path(gsNode) + "/z/K/o")}
            core.set_pointer(gsNode, "currentMove", childNode)
            curMoveNode = {"rootId": gsNode.get("rootId"), "nodePath": core.get_pointer_path(gsNode, "currentMove")}
        
        #logger.info(curMoveNode)
        
        curMovePar = core.get_parent(curMoveNode)
        currentGS["currentMove"] = {"color": core.get_attribute(curMoveNode, "color"),
                                    "row": core.get_attribute(curMovePar, "row"),
                                    "column": core.get_attribute(curMovePar, "column")}
        
        # Get board node
        boardNode = core.get_parent(curMovePar)
        boardTiles = core.load_sub_tree(boardNode)
        
        # Fill board with 0s so we can replace with dicts; this is done to ensure everything is in row/column order
        board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        for tile in boardTiles:
            if (core.is_instance_of(tile, META['Tile'])):
                rowNum = core.get_attribute(tile, "row")
                colNum = core.get_attribute(tile, "column")
                curTile = {}
                cPaths = core.get_children_paths(tile)
                if (len(cPaths) == 0):
                    curTile["color"] = "none"
                else:
                    # Get child piece node to get its color
                    childColorNode = {"rootId": active_node.get("rootId"), "nodePath": cPaths[0]}
                    color = str(core.get_attribute(childColorNode, "color"))
                    #logger.info(color)
                    curTile["color"] = color
                    #logger.error(curTile["color"] + " " + str(rowNum) + " " + str(colNum))
                
                isValid = core.get_attribute(tile, "isValid")
                curTile["isValid"] = isValid
                curTile["flips"] = []
                board[rowNum][colNum] = curTile
                
                if (isValid):
                    dictKey = str(rowNum) + " " + str(colNum)
                    for chain in flips[dictKey]:
                        board[rowNum][colNum]["flips"].append(chain)
            
        currentGS["board"] = board
        
        gameObj.append(currentGS)   
        
        # Print in json format
        logger.info(json.dumps(gameObj, indent = 2))
        
        #self.util.save(self.root_node, self.commit_hash, self.branch_name, 'New GS created')
        
        #rowFlip = 2
        #colFlip = 3
        #chains = gameObj[0]["board"][rowFlip][colFlip]["flips"]
        #logger.error(chains)

        self.create_message(active_node, json.dumps(gameObj))
        
        #flip([rowFlip, colFlip], chains)
        #undo()
        #auto()