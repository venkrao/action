from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.functions import Now


# Create your models here.
class Language(models.Model):
    language = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.language


class CourseCategory(models.Model):
    category = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.category


class CourseSubcategory(models.Model):
    class IdealForUserType(models.TextChoices):
        beginner = 'beginner', _("Beginner")
        advanced = 'advanced', _("Advanced")
        all = 'all', _("All")

    class RecommendedClassFrequency(models.TextChoices):
        one_to_three_times_per_week = '1-3 X/week'
        two_to_four_times_per_week = '2-3 X/week'

    category = models.ForeignKey(CourseCategory,
                                 on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=32)
    catchphrase = models.CharField(max_length=126)
    short_description = models.CharField(max_length=32)
    long_description = models.CharField(max_length=256)
    offered_in_languages = models.ForeignKey(Language, on_delete=models.CASCADE)
    ideal_for = models.CharField(max_length=10, choices=IdealForUserType.choices)
    recommended_class_frequency = models.CharField(max_length=20, choices=RecommendedClassFrequency.choices)
    what_to_expect = models.CharField(max_length=128)
    what_you_need_for_class = models.CharField(max_length=128)

    class Meta:
        unique_together = ['subcategory', 'offered_in_languages']

    def __str__(self):
        return "{}-{}".format(self.subcategory, self.offered_in_languages)


class SessionPackageOffering(models.Model):
    class SessionSize(models.TextChoices):
        small = "Small", _("Small")
        medium = "Medium", _("Medium")
        large = "Large", _("Large")

    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    course_subcategory = models.ForeignKey(CourseSubcategory, on_delete=models.CASCADE)
    session_size = models.TextField(max_length=10, choices=SessionSize.choices)
    number_of_sessions = models.IntegerField()
    price_per_session = models.FloatField(max_length=6)
    total_price = models.FloatField(max_length=7)

    class Meta:
        unique_together = ['course_category', 'course_subcategory', 'session_size']

    def __str__(self):
        return "{}-{}".format(self.course_subcategory, self.session_size)


class Coach(models.Model):
    class Gender(models.TextChoices):
        male = 'Male', _("Male")
        female = 'Female', _("Female")

    username = models.CharField(max_length=12, unique=True)
    display_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=60)
    gender = models.CharField(max_length=6,
                              choices=Gender.choices)
    about_me = models.CharField(max_length=256)

    def __str__(self):
        return "{}".format(self.display_name)


class ActioSession(models.Model):
    class SessionStatus(models.TextChoices):
        scheduled = 'Scheduled', _("Scheduled")
        completed = 'Completed', _("Completed")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    course_subcategory = models.ForeignKey(CourseSubcategory, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    conducted_on = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    session_status = models.CharField(max_length=10, choices=SessionStatus.choices)

    def __str__(self):
        return "Coach: {}-User: {}-Date: {}-Course:{}-Status:{}".format(self.coach, self.user, self.conducted_on,
                                                              self.course_subcategory, self.session_status)

    class Meta:
        unique_together = [ 'coach', 'user', 'start_time', 'end_time', 'conducted_on']


class TwilioRoom(models.Model):
    actio_session = models.ForeignKey(ActioSession, on_delete=models.CASCADE)
    unique_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    access_token = models.CharField(max_length=600, null=True)
    date_created = models.DateTimeField(default=Now)


class AmazonResourceName(models.Model):
    """ Contains the AWS ARN endpoints for each user on Twilio. The ARN are used to send push notifications """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    arn = models.CharField(max_length=256)

    class Meta:
        unique_together = ["user", "arn"]

    def __str__(self):
        return "{}-{}".format(self.user, self.arn)