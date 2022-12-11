# Import UserActionsBase to extend it.
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase


# Your class must extend UserActionsBase.
class SkarControls(UserActionsBase):

    # Your class must implement this method.
    def create_actions(self):
        self.add_global_action('potato', self.potato)
        self.add_global_action('col', self.colorSelectedTrack)
        self.add_global_action('next', self.nextTrack)
        self.add_global_action('prev', self.prevTrack)
        self.add_global_action('recplay', self.recordOrPlay)
        self.add_global_action('playStop', self.stopOrPlay)
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

    def recordOrPlay(self, action_def, args):
        self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/arm on')
        track = self.song().view.selected_track
        cliplist = list(track.clip_slots)
        for clip in track.clip_slots:
            self.log('looping through clips, %s' % clip)
            self.log('clip index, %s' % cliplist.index(clip))
            if clip.has_clip:
                self.log('clip exists')
            elif cliplist.index(clip) == 0:
                self.log('index is 0')
                clipslot = cliplist.index(clip)  # no clips -> select first empty clipslot
                break
            else:
                self.log('else')
                clipslot = cliplist.index(clip) - 1  # clips exist -> select last clip
                break
        if track.clip_slots[clipslot].is_recording:
            self.log('is recording! start playing')
            # self.canonical_parent.clyphx_pro_component.trigger_action_list('SEL/arm off')  # causes audio and midi to cut out
        elif track.clip_slots[clipslot].has_clip:
            self.log('not recording, start recording on next slot')
            clipslot += 1
        action = 'SEL/play %s' % (clipslot + 1)
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action)

    def stopOrPlay(self, action_def, args):
        track = self.song().view.selected_track
        cliplist = list(track.clip_slots)
        for clip in track.clip_slots:
            if clip.has_clip:
                self.log('clip exists')
            elif cliplist.index(clip) == 0:
                self.log('index is 0 - do nothing')
                return
            else:
                self.log('else')
                clipslot = cliplist.index(clip) - 1  # clips exist -> select last clip
                break
        if track.clip_slots[clipslot].is_recording:
            self.log('is recording! stop playback')
            action = 'SEL/stop %s' % (clipslot + 1)
        elif track.clip_slots[clipslot].is_playing == 1:
            self.log('clip playing, stop playback')
            action = 'SEL/stop %s' % (clipslot + 1)
        else:
            self.log('not playing, start playback')
            action = 'SEL/play %s' % (clipslot + 1)

        self.canonical_parent.clyphx_pro_component.trigger_action_list(action)

    def log(self, message):
        self.canonical_parent.log_message(message)
