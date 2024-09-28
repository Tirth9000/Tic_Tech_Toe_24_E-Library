from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class LibraryUser(models.Model):
    userid = models.CharField(primary_key=True, max_length=6)
    password = models.CharField(max_length=30)
    username = models.CharField(max_length=40)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=40)
    
    def __str__(self):
        return self.userid


class Books(models.Model):
    userid = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    fileID = models.CharField(primary_key=True, max_length=6)
    book_pdf = models.FileField(upload_to='Media/book', default=None)
    bookDescription = models.TextField()
    author = models.CharField(max_length=40)
    public = models.DateTimeField()
    category = models.CharField(max_length=30)
    avg_rating = models.FloatField(default=0)
    
    def __str__(self):
        return self.fileID

class Rating(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)   
    feedback = models.TextField()
    
    
class FavouriteCollections(models.Model):
    fav_book = models.OneToOneField(Books, on_delete=models.CASCADE)
    userid = models.CharField(max_length=6)


    

def set_password(raw_password):
    return make_password(raw_password)


def user_authenticate(userid, password):
    try:
        user = LibraryUser.objects.get(userid=userid)
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