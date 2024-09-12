## ================================= Limit and Priority class =================================
class LimitsAndPriority:
    def __init__(self):
        self.bitrate = None
        self.audio_format_priority = None
        self.resolution = None
        self.fps = None
        self.video_format_priority = None
    #end

    def setLimitsToMax(self):
        # Internal conversion method
        self.bitrate = "max kbps"
        self.resolution = "max p"
        self.fps = propToInt(self.fps,"max fps")
    #end

    def to_numeric(self):
        # Internal conversion method
        self.bitrate = propToInt(self.bitrate,"kbps")
        self.resolution = propToInt(self.resolution,"p")
        self.fps = propToInt(self.fps,"fps")
    #end
#end


## ================================= Helper functions =================================
def propToInt(prop,str):
    intProp = prop.split(str)[0].strip()
    try:
        intProp = int(intProp)
        return intProp
    except (TypeError, ValueError):
        pass
    #end
    return prop
#end


def get_variable_names(cls):
    return list(cls.__annotations__.keys())
#end

def get_variable_types(cls):
    return list(cls.__annotations__.values())
#end
