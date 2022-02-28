from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm
)
from .models import User,ModelItemList

# 
# 商品情報フォーム
# 
class itemForm(forms.ModelForm):
    '''商品情報フォーム'''
    class Meta:
        model = ModelItemList
        fields = (
            'image1', 
            'name',
            'price',
            'category',
            'status',
            'description',
            'bearShippingFee',
            'shippingFee',
            'shippingMethod',
            'shipArea',
            'shippingTime',
            )
        labels={
           'image1':'画像1',
           'name':'商品名',
           'price':'金額',
           'category':'カテゴリー',
           'status':'商品の状態',
           'description':'商品の詳細',
           'bearShippingFee':'送料負担',
           'shippingFee':'送料',
           'shippingMethod':'配送方法',
           'shipArea':'発送元の地域',
           'shippingTime':'発送までの日数',
           }
        widgets = {
            'image1': forms.ClearableFileInput(attrs={'multiple': True}),
            }

# 
# 利用者情報フォーム
# 
User = get_user_model()
class userCreateForm(UserCreationForm):
    """利用者情報登録フォーム"""
    class Meta:
        model = User
        if User.USERNAME_FIELD == 'email':
            fields = ('email',)
        else:
            fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class userUpdateForm(forms.ModelForm):
    '''利用者情報更新フォーム'''
    class Meta:
        model = User
        fields = (
            'name',
            'description'
            )
        labels={
           'name':'ユーザ名',
           'description':'自己紹介',
           }
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'cols':30}),
        }

# 
# パスワードフォーム
# 
class passwordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class passwordResetForm(PasswordResetForm):
    """パスワードリセットフォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'