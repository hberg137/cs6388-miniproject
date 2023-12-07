"""
This is where the implementation of the plugin code goes.
The AutoPlace-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import os
import logging
from webgme_bindings import PluginBase

# Set path for modules
sys.path.append('.')
from src.plugins.ValidTiles.ValidTiles import ValidTiles
from src.plugins.FlipTiles.FlipTiles import FlipTiles

# Setup a logger
logger = logging.getLogger('AutoPlace')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class AutoPlace(PluginBase):
    def main(self):
        active_node = self.active_node
        core = self.core

        gsNode = {"rootId": active_node.get("rootId"), "nodePath": core.get_pointer_path(active_node, "currentState")}
        flips = ValidTiles.main(self)
        # Choose the first valid tile
        for key in flips:
            pos = [int(key[0]), int(key[-1])]
            logger.warn(pos)
            chains = flips[key]
            logger.warn(chains)
            break
        
        FlipTiles.main(self, pos, chains)
