from datetime import timezone
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class LibraryUser(models.Model):
    userid = models.CharField(primary_key=True, max_length=6)
    password = models.CharField(max_length=30)
    username = models.CharField(max_length=40)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=40)
    photo = models.FileField(upload_to='profile_pic/', default='default/default_image.jpeg' )
    
    def __str__(self):
        return self.userid


class Books(models.Model):
    CHATEGORY_CHOICES = (
        ('lang', 'Languages'),
        ('webdev', 'Web Development'),
        ('dbms', 'DBMS'),
        ('ai/ml', 'AI/ML'),
        ('CS', 'Cyber Security'),
        ('iot', 'IOT'),
        ('dsa', 'DSA'),
        ('Others', 'Others'),
    )
    userid = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    fileID = models.CharField(primary_key=True, max_length=6)
    book_title = models.CharField(max_length=40, default=None)
    book_photo = models.FileField(upload_to='books_photos/', default=None)
    book_pdf = models.FileField(upload_to='books_pdf/', default=None)
    bookDescription = models.TextField()
    author = models.CharField(max_length=40)
    publish = models.DateTimeField(auto_now=True )
    category = models.CharField(max_length=100, choices=CHATEGORY_CHOICES, default='Others')
    avg_rating = models.FloatField(default=0)
    
    def __str__(self):
        return self.fileID

class Rating(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)   
    feedback = models.TextField()
    
# class FavouriteBooks(models.Model):
#     user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
#     book = models.ForeignKey(Books, on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.id)
class FavouritiesBooks(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return str(self.user)

    

def set_password(raw_password):
    return make_password(raw_password)


def user_authenticate(useremail, password):
    try:
        user = LibraryUser.objects.get(email=useremail)
        if check_password(password, user.password):
            return user
        else:
            return None
    except LibraryUser.DoesNotExist:
        return None


def CheckPassword(password):
    special_char = ['/', '[', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', '?', ':', '{', '}', '|', '<', '>', ']']
    if len(password) < 8:
        return True
    elif " " in password.strip():
        return True
    else:
        upper_flag = 0
        lower_flag = 0
        digit_flag = 0
        special_flag = 0
        for char in password:
            if char in special_char:
                special_flag += 1
                continue
            elif char.isdigit():
                digit_flag += 1
                continue
            elif char.islower():
                lower_flag += 1
                continue
            elif char.isupper():
                upper_flag += 1
                continue
            else:
                continue
            
        if (upper_flag == 0 or lower_flag == 0) or (digit_flag == 0 or special_flag == 0):
            return True
    return False