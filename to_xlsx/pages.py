class page_info(object):
    def __init__(self):
        self.index = []
        self.classroom = []
        self.subject = []
        self.is_video = []
        self.data_type = []
        self.title_jp = []
        self.title_en = []
        self.bio = []
        self.bio_type = []
        self.capture_date = []
        self.capture_time = []
        self.capture_place = []
        self.keywords = []
        self.condition = []
        self.is_opened = []
        self.comment_jp = []
        self.comment_en = []
        self.reference = []
        self.editor_name = []

class bio_info(object):
    def __init__(self):
        self.phylum = []
        self.bio_class = []
        self.name_jp = []
        self.name_en = []

class capture_info(object):
    def __init__(self):
        self.place_type = []
        self.is_local = []
        self.location_1 = []
        self.location_2 = []

class condition_info(object):
    def __init__(self):
        self.use_micro = []
        self.use_auto = []
        self.use_probe = []
        self.use_infrared = []
        self.capture_interval = []
        self.capture_speed = []
        self.photographer = []
        self.copyright = []
