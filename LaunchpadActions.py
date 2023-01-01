# Import UserActionsBase to extend it.
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase


# Your class must extend UserActionsBase.
class LaunchpadActions(UserActionsBase):

    # Your class must implement this method.
    def create_actions(self):
        self.add_global_action('potato', self.potato)
        self.add_global_action('col', self.colorSelectedTrack)
        self.add_global_action('next', self.nextTrack)
        self.add_global_action('prev', self.prevTrack)
        self.add_track_action('test', self.test)

    def potato(self, action_def, args):
        self.canonical_parent.show_message("hello hello")
        self.canonical_parent.log_message("log message log log")

    def colorSelectedTrack(self, action_def, args):
        self.log(args)
        action1 = 'SEL/color %s' % args
        action2 = 'SEL/CLIP(ALL) color %s' % args
        action = action1 + ' ; ' + action2
        self.log(action1 + ' ; ' + action2)
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action)

    def test(self, action_def, args):
        self.log("test1")
        track = action_def['track']
        self.log(track)
        cliplist = list(track.arrangement_clips)  # won't work without ableton live 11 :(
        self.log("test3")

    def nextTrack(self, action_def, args):
        if self.application().view.is_view_visible('Session'):
            action = 'RIGHT'
        else:
            action = 'DOWN'
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action)

    def prevTrack(self, action_def, args):
        if self.application().view.is_view_visible('Session'):
            action = 'LEFT'
        else:
            action = 'UP'
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action)

    def log(self, message):
        self.canonical_parent.log_message(message)
