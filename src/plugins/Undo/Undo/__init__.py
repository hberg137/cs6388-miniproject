"""
This is where the implementation of the plugin code goes.
The Undo-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('Undo')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Undo(PluginBase):
    def main(self):
        active_node = self.active_node
        core = self.core
        
        gsNode = {"rootId": active_node.get("rootId"), "nodePath": core.get_pointer_path(active_node, "currentState")}
        prevNode = {"rootId": gsNode.get("rootId"), "nodePath": core.get_pointer_path(gsNode, "previousState")}
        if prevNode["nodePath"] == None:
            return
        core.set_pointer(active_node, "currentState", prevNode)
        core.delete_node(gsNode)
        
        self.util.save(self.root_node, self.commit_hash, self.branch_name, 'Undo GS')
