from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager 

# Create your models here.


class UserManager(BaseUserManager):
    """
    ユーザーマネージャー
    """

    user_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        メールアドレスでの登録を必須にする
        """
        if not email:
            raise ValueError("The given email must be set.")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        is_staff, is_superuserをFalseに
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        superuserはis_staff, us_superuserをTrueに
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    カスタムユーザーモデル
    """

    email = models.EmailField(_('メールアドレス'), unique=True)
    full_name = models.CharField(_('氏名'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('スタッフ'),
        default=False,
        help_text=_(
            '管理者サイトにログインできるか'
        )
    )

    is_superuser = models.BooleanField(
        _('スーパーユーザー'),
        default=False,
        help_text=_(
            'スーパーユーザーかどうか'
        )
    )

    is_active = models.BooleanField(
        _('アクティブ'),
        default=True,
        help_text=_(
            'ユーザーがアクティブかどうか'
        )
    )

    dete_joined = models.DateTimeField(_('登録日'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def get_full_name(self):
        """
        氏名を返す
        """
        return self.full_name
    
    def get_short_name(self):
        """
        短縮した氏名を返す
        """
        return self.full_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        このユーザーにメールを送る
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """
        username属性のゲッター
        """

        return self.email