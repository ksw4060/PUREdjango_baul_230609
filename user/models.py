from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):
    # 유저를 생성하는 함수
    def create_user(self, email, account, username, introduction, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        # 유저를 생성할 때, 입력해야 하는 값들 + 비밀번호는 무조건 입력해야함
        user = self.model(
            email=self.normalize_email(email),
            account=account,
            username=username,
            introduction=introduction,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    # 슈퍼 유저를 생성하는 함수. python3 manage.py createsuperuser 할때
    def create_superuser(self, email, account, username, introduction, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        # 슈퍼 유저를 생성할 때, 입력해야 하는 값들 + 비밀번호는 무조건 입력해야함
        user = self.create_user(
            email,
            password=password,
            account=account,
            username=username,
            introduction=introduction,
        )
        user.is_admin = True # 슈퍼 유저는 관리자 권한이 있음
        user.save(using=self._db)
        return user


class UserModel(AbstractUser):

    class Meta:
        db_table = "user" # 여기는 테이블 이름

    account = models.CharField("계정이름", null=False, max_length=50, unique=True)
    email = models.EmailField("이메일", max_length=255, unique=True)
    username = models.CharField("유저이름", null=False, blank=False, max_length=50)
    introduction = models.TextField("자기소개", null=True, blank=True)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
    created_at = models.DateField("계정 생성일", auto_now_add=True)
    is_active = models.BooleanField("활성화 여부", default=True)
    is_admin = models.BooleanField("관리자 여부", default=False)

    objects = UserManager() #쿼리셋 매니저가 UserManager임을 밝힘
    # USERNAME_FIELD 와 REQUIRED_FIELDS는 유저를 생성할 때, 필요한 필드이기 때문에 create_user 및 create_superuser시 필드를 추가시켜 줘야 함
    USERNAME_FIELD = 'account' # 회원가입시, 계정이름으로 가입하기 때문에, Unique=True 로 해주어야 하는 필드
    REQUIRED_FIELDS = ['email', 'username', 'introduction',]


    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
