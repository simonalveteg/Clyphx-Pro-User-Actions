# Import UserActionsBase to extend it.
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase


# Your class must extend UserActionsBase.
class SkarControls(UserActionsBase):

    # Your class must implement this method.
    def create_actions(self):
        self.add_global_action('potato',self.potato)

    def potato(self,action_def,args):
        self.canonical_parent.show_message("hello hello")
        self.canonical_parent.log_message("log message log log")
