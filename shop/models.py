from statistics import mode
from sqlalchemy import true
from datetime import date
import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager,
    PermissionsMixin
)
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.db import models
# from .models import ModelTransactionList

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """利用者情報モデル"""
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    name = models.CharField('name', max_length=32, default='NoName')
    picture = models.ImageField('picture', max_length=2000, blank=True, null=True, upload_to='media')
    description = models.CharField('description', max_length=4000, blank=True)
    # 住所
    # 支払い情報
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class ModelItemCondition(models.Model):
    """商品状態"""
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('状態', max_length=40)

    def __str__(self):
        return self.value

class ModelShippingMethod(models.Model):
    """配送方法"""
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('配送方法', max_length=40)

    def __str__(self):
        return self.value

class ModelBearShippingFee(models.Model):
    """送料負担"""
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('送料負担', max_length=40)

    def __str__(self):
        return self.value

class ModelArea(models.Model):
    """発送元地域"""
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('地域', max_length=40)

    def __str__(self):
        return self.value

class ModelShippingTime(models.Model):
    """発送までの日数"""
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('発送までの日数', max_length=40)

    def __str__(self):
        return self.value

class ModelItemCategory(models.Model):
    """商品カテゴリー"""
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('商品カテゴリー', max_length=40)

    def __str__(self):
        return self.value

class ModelItemCategoryDetail(models.Model):
    """商品詳細カテゴリー"""
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('詳細カテゴリー', max_length=40)

    def __str__(self):
        return self.value

class ModelListStatus(models.Model):
    """出品状態"""
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('出品状態', max_length=40)

    def __str__(self):
        return self.value

class ModelShipStatus(models.Model):
    """配送状態"""
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('配送状態', max_length=40)

    def __str__(self):
        return self.value

class ModelTransactionStatus(models.Model):
    """取引状態"""
    id = models.IntegerField('ID', primary_key=True)
    value = models.CharField('取引状態', max_length=40)

    def __str__(self):
        return self.value

class ModelItemList(models.Model):
    """商品一覧モデル"""
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4, editable=False)
    image1 = models.ImageField('画像1', null=True, blank=True, upload_to='media')
    image2 = models.CharField('画像2', max_length=300, blank=True)
    image3 = models.CharField('画像3', max_length=300, blank=True)
    image4 = models.CharField('画像4', max_length=300, blank=True)
    image5 = models.CharField('画像5', max_length=300, blank=True)
    image6 = models.CharField('画像6', max_length=300, blank=True)
    image7 = models.CharField('画像7', max_length=300, blank=True)
    image8 = models.CharField('画像8', max_length=300, blank=True)
    image9 = models.CharField('画像9', max_length=300, blank=True)
    image10 = models.CharField('画像10', max_length=300, blank=True)
    name = models.CharField('商品名', max_length=80)
    price = models.IntegerField('値段')
    status = models.ForeignKey(ModelItemCondition, verbose_name='商品状態', max_length=1, on_delete=models.CASCADE)
    description = models.CharField('商品説明', max_length=2000)
    shippingMethod = models.ForeignKey(ModelShippingMethod,verbose_name='配送方法', max_length=2, on_delete=models.CASCADE)
    shippingFee = models.IntegerField('送料', blank=True)
    bearShippingFee = models.ForeignKey(ModelBearShippingFee,verbose_name='送料負担', max_length=1, on_delete=models.CASCADE)
    category = models.ForeignKey(ModelItemCategory,verbose_name='カテゴリー', max_length=4, on_delete=models.CASCADE)
    shipArea = models.ForeignKey(ModelArea,verbose_name='発送元地域', max_length=2, on_delete=models.CASCADE)
    shippingTime = models.ForeignKey(ModelShippingTime,verbose_name='発送までの日数', max_length=1, on_delete=models.CASCADE)
    sellDate = models.DateTimeField('出品日')
    seller = models.ForeignKey(User,verbose_name='出品者', max_length=8, related_name='seller', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User,verbose_name='購入者', max_length=8, related_name='buyer', blank=True, null=True, on_delete=models.CASCADE)
    lastUpdate = models.DateTimeField('最終更新日')
    listStatus = models.ForeignKey(ModelListStatus,verbose_name='出品状態', max_length=1, default=0, on_delete=models.CASCADE)
    shipStatus = models.ForeignKey(ModelShipStatus, verbose_name='配送状態', default=0, on_delete=models.CASCADE)
    transactionStartDate = models.DateTimeField('取引開始日', blank=True, null=True)
    transactionStatus = models.ForeignKey(ModelTransactionStatus, verbose_name='取引状態', default=0, on_delete=models.CASCADE)

    def __str__(self):
        return self.name