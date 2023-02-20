# Import UserActionsBase to extend it.
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

import traceback

def print_except(func):
    def inner(*args, **kwargs):
      try:
        func(*args, **kwargs)
      except:
        args[0].canonical_parent.log_message(traceback.format_exc())
    return inner


class LivesetActions(UserActionsBase):
    """ ExampleActions provides some example actions for demonstration purposes. """

    # Your class must implement this method.
    def create_actions(self):
        self.add_track_action('rp', self.rec)
        self.add_track_action('pp', self.pause)
        self.add_global_action('duplicate', self.duplicate)
        self.add_track_action('col', self.colorTrack)
        self.add_global_action('clr_session', self.clearSession)


    @print_except
    def clearSession(self, action_def, args):
        tracks = list(self.song().tracks)
        for track in tracks:
            clips = list(track.clip_slots)
            for clipslot in clips:
                if clipslot.has_clip:
                    clipslot.delete_clip()
        
    @print_except
    def rec(self, action_def, args):
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
                clipslot = cliplist.index(clip)  # no clips -> select first empty clipslot
                break
            else:
                self.log('else')
                clipslot = cliplist.index(clip) - 1  # clips exist -> select last clip
                break
        self.log('playing_status: %s' % track.clip_slots[clipslot].playing_status)
        self.log('is_recording: %s' % track.clip_slots[clipslot].is_recording)
        if track.clip_slots[clipslot].is_recording:
            self.log('is recording! start playing')
        elif track.clip_slots[clipslot].has_clip:
            self.log('not recording, start recording on next slot')
            clipslot += 1

        action = '%s/play %s' % (track_index, clipslot + 1)
        self.triggerActionList(action)

    @print_except
    def pause(self, action_def, args):
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
                clipslot = cliplist.index(clip) - 1  # clips exist -> select last clip
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

        self.triggerActionList(action)

    @print_except
    def duplicate(self, action_def, args):
        tracks = list(self.song().tracks)
        selTrack = self.song().view.selected_track
        selTrackIndex = tracks.index(selTrack)
        trackArmed = selTrack.arm
        self.song().duplicate_track(selTrackIndex)
        newTrack = list(self.song().tracks)[selTrackIndex+1]
        if trackArmed:
            selTrack.arm = False
            newTrack.arm = True
        for clip in list(newTrack.clip_slots):
            if clip.has_clip:
                clip.delete_clip()

    @print_except
    def colorTrack(self, action_def, args):
        track = action_def['track']
        currentColor = track.color_index
        colors = [22, 17, 26, 47, 24, 20, 14, 69]
        newColor = colors[0]
        if currentColor in colors:
            index = colors.index(currentColor)+1
            if index >= len(colors):
                index = 0
            newColor = colors[index]

        track.color_index = newColor
        for clip in list(track.clip_slots):
            if clip.has_clip:
                clip.clip.color_index = newColor
        for clip in list(track.arrangement_clips):
                clip.color_index = newColor

    def toast(self, comments):
        self.canonical_parent.show_message(comments)

    def log(self, message):
        self.canonical_parent.log_message(message)

    def triggerActionList(self, list):
        self.canonical_parent.clyphx_pro_component.trigger_action_list(list)