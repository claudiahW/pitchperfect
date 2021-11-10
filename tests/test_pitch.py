from app.models import Pitch
from app import db

def setUp(self):
    self.new_pitch = Pitch(1,'test pass','Marketing','2020-09-22 06:53:12.713576',20,10)
    
def test_check_instance_variables(self):
    self.assertEquals(self.new_pitch.id,1)
    self.assertEquals(self.new_pitch.pitch,'test pass')
    self.assertEquals(self.new_pitch.category,"Marketing")
    self.assertEquals(self.new_pitch.posted,'2020-09-22 06:53:12.713576')
    self.assertEquals(self.new_pitch.like,20)
    self.assertEquals(self.new_pitch.dislike,10)
    
def test_save_pitch(self):
    self.new_pitch.save_pitch()
    self.assertTrue(len(Pitch.query.all())>0)
    
def test_get_pitch_by_id(self):

    self.new_pitch.save_pitch()
    got_pitch = Pitch.get_pitch(1)
    self.assertTrue(len(got_pitch) == 1)
    