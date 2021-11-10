from app.models import Review,User
from app import db 

def setUp(self):
        self.user_James = User(username = 'james',password = 'potato', email = 'james@ms.com')
        self.new_review = Review(pitch_id=12345,pitch_title='Review for pitch',image_path="https://image.tmdb.org/t/p/w500/jdjdjdjn",pitch_review='This pitch is the best thing since sliced bread',user = self.user_James )

def test_save_review(self):
        self.new_review.save_review()
        self.assertTrue(len(Review.query.all())>0)        

def test_get_review_by_id(self):

        self.new_review.save_review()
        got_reviews = Review.get_reviews(12345)
        self.assertTrue(len(got_reviews) == 1)        