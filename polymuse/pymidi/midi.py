
from rmidi.constant import meta_event_format, ch_event_format, sys_event_format, event_format

import mutils

import numpy

class Midi:
    def __init__(self,   format_type = 0, track_count = 0, time_div = 0x1e0, filename = None ):
        self.format_type = format_type
        self.track_count = track_count
        self.time_div = time_div
        self.tracks = [Track(self.to_dict()) for _ in range(track_count)] 
        pass
    def to_dict(self, header = True):
        if header : return {format_type : self.format_type, track_count : self.track_count, time_div: self.time_div}
        else : raise NotImplementedError("to_dict only returns header : True for now")

class Track:
    def __init__(self, midi_header, **ch_events):
        self.midi_header = midi_header
        self.ch_events = {}
        
        self.note = []
        pass

    def set_channel_events(self, ch_events = {}):
        events = {}
        for ev_name, ch_ev in ch_events.items():
            pass


class Event:
    def __init__(self, time, event):
        self.time = time
        if type(event) == str: event_info = mutils.find(event_format, event)
        elif type(event) == int and 0x7F < event < 0x100: mutils.find(event_format, event)#event_info = event_format[str(event)]
        self.event_id = event_info.id
        self.name  = event_info.name

class ChannelEvents(Event):
    def __init__(self, time, event_id, **data):
        super().__init__(time, event_id)
        event_info = ch_event_format[str(self.event_id)]
        for ev, v in data.items():
            pass

class MetaEvents(Event):
    def __init__(self, time, event_id):
        super().__init__(time, event_id)

class SysEvents(Event):
    def __init__(self, time, event_id):
        super().__init__(time, event_id)


class Note:
    def __init__(self, time, note, intensity, duration, pitch_bend = 0):
        self.time = time
        self.note = note
        self.intensity = intensity
        self.duration = duration
        self.pitch_bend = pitch_bend
        pass

class Group:
    def __init__(self, *notes):
        if numpy.isscalar(notes) : return
        self.notes = notes
        pass

class Chord(Group):
    def __init__(self, *notes):
        super().__init__(*notes)
