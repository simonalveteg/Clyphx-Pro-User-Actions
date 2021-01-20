# Import UserActionsBase to extend it.
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase


# Your class must extend UserActionsBase.
class ExampleActions(UserActionsBase):

    # Your class must implement this method.
    def create_actions(self):
        self.add_track_action('rp', self.sa_rec)
        self.add_track_action('pp', self.sa_pause)
        self.add_global_action('drums', self.sa_drums)
        self.add_global_action('tt', self.sa_test)

    def sa_drums(self, action_def, args):
        """ finds the right clip in 'drums' track and plays it"""
        self.toast(args)
        action = '\"DRUMS\"/play \"%s\"' % args
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action)

    def sa_rec(self, action_def, args):
        """check if track is already recording, play clip (to stop recording) if it is, otherwise start recording"""
        track = action_def['track']
        tracklist = list(self.song().tracks)
        track_index = tracklist.index(track) + 1
        cliplist = list(track.clip_slots)
        self.log('Called on track no: %s' % track_index)
        for clip in track.clip_slots:
            self.log('looping through clips, %s' % clip)
            self.log('clip index, %s' % cliplist.index(clip))
            if clip.has_clip:
                self.log('clip exists')
            elif cliplist.index(clip) == 0:
                self.log('index is 0')
                clipslot = cliplist.index(clip) # no clips -> select first empty clipslot
                break
            else:
                self.log('else')
                clipslot = cliplist.index(clip) - 1 # clips exist -> select last clip
                break
        self.log('playing_status: %s' % track.clip_slots[clipslot].playing_status)
        self.log('is_recording: %s' % track.clip_slots[clipslot].is_recording)
        if track.clip_slots[clipslot].is_recording:
            self.log('is recording! start playing')
        elif track.clip_slots[clipslot].has_clip:
            self.log('not recording, start recording on next slot')
            clipslot += 1

        action = '%s/play %s' % (track_index, clipslot + 1)
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action)

    def sa_pause(self, action_def, args):
        """ play/stop the latest clip. If clip is recording it should stop the clip. if no clip exists do nothing """
        track = action_def['track']
        tracklist = list(self.song().tracks)
        track_index = tracklist.index(track) + 1
        cliplist = list(track.clip_slots)
        self.log('Called on track no: %s' % track_index)
        for clip in track.clip_slots:
            self.log('looping through clips, %s' % clip)
            self.log('clip index, %s' % cliplist.index(clip))
            if clip.has_clip:
                self.log('clip exists')
            elif cliplist.index(clip) == 0:
                self.log('index is 0 - do nothing')
                return
            else:
                self.log('else')
                clipslot = cliplist.index(clip) - 1 # clips exist -> select last clip
                break
        if track.clip_slots[clipslot].is_recording:
            self.log('is recording! stop playback')
            action = '%s/stop %s' % (track_index, clipslot + 1)
        elif track.clip_slots[clipslot].is_playing == 1:
            self.log('clip playing, stop playback')
            action = '%s/stop %s' % (track_index, clipslot + 1)
        else:
            self.log('not playing, start playback')
            action = '%s/play %s' % (track_index, clipslot + 1)

        self.canonical_parent.clyphx_pro_component.trigger_action_list(action)

        def sa_test(self, action_def, args):
            """find playing clip on track y and select it. """
            tracklist = list(self.song().tracks)
            self.log('start')
            y = args
            # vars = args.split()
            # y = args[0]
            self.log(y)
            for track in tracklist:
                self.log('looping: %s' % track.name)
                if track.name == y:
                    self.log('track %s found' % track.name)
                    t = track
                    if t.playing_slot_index >= 0:
                        self.log('has playing clip: %s' % t.playing_slot_index)
                        selection = t.playing_slot_index + 1 # first clip has index 0
                        self.canonical_parent.clyphx_pro_component.trigger_action_list('metro')
                        self.canonical_parent.clyphx_pro_component.trigger_action_list('\"%s\"/sel %s' % (y, selection))
                    break

    def toast(self, comments):
        self.canonical_parent.show_message(comments)
    def log(self, message):
        self.canonical_parent.log_message(message)
