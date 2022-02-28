from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

app_name = 'shop'
urlpatterns = [
    # トップページ(商品一覧)
    path('', views.ViewItemList.as_view(), name='top'),

    # 
    # 商品情報
    # 
    # 商品情報登録
    path('sell/', views.ViewCreateItem, name='createItem'),
    # 商品情報詳細
    path('item/<uuid:id>', views.ViewReadItem, name='readItem'),
    # 商品情報変更
    path('updateItem/<slug:id>', views.ViewUpdateItem, name='updateItem'),
    path('updateItemComplete/<slug:id>', views.ViewUpdateItemComplete, name='updateItemComplete'),
    # 商品情報削除
    path('deleteItem/<slug:id>', views.ViewDeleteItem, name='deleteItem'),

    # 
    # 利用者情報
    # 
    # 利用者情報登録
    path('signup/', views.SignUpView.as_view(), name='createUser'),
    # 利用者情報詳細
    path('user/<int:id>', views.ViewReadUser, name='readUser'),
    # 利用者情報変更
    path('editUser', views.ViewUpdateUser, name='updateUser'),
    path('updateUser', views.ViewUpdateUserComplete, name='updateUserComplete'),
    # 利用者情報削除(退会)
    path('deleteUserConfirm', TemplateView.as_view(template_name='shop/TempDeleteUserConfirm.html'), name='deleteUserConfirm'),
    path('deleteUserComplete', views.DeleteView.as_view(), name='deleteUserComplete'),

    # 
    # ログイン / ログアウト / マイページ
    # 
    # ログイン
    path('login/', views.LoginView.as_view(), name='login'),
    # ログアウト
    path('logout/', views.Logout.as_view(), name='logout'),
    # マイページ
    path('mypage/', views.ProfileView.as_view(), name='mypage'),

    # 
    # パスワード
    # 
    # パスワード変更
    path('passwordChange/', views.PasswordChange.as_view(), name='passwordChange'),
    path('passwordChangeDone/', views.PasswordChangeDone.as_view(), name='passwordChangeDone'),

    # パスワードリセット
    path('passwordResetForm/', views.passwordResetForm.as_view(), name='passwordResetForm'),
    path('passwordResetDone/', views.passwordResetDone.as_view(), name='passwordResetDone'),
    path('passwordResetEmail/', views.passwordResetEmail.as_view(), name='passwordResetEmail'),
    path('passwordResetConfirm/<uidb64>/<token>/', views.passwordResetConfirm.as_view(), name='passwordResetConfirm'),
    path('passwordResetComplete/', views.passwordResetComplete.as_view(), name='passwordResetComplete'),

    # 
    # 商品取引
    # 
    # 商品購入
    path('purchase/<uuid:id>', views.ViewPurchase, name='purchase'),
    path('purchaseComplete/<uuid:id>', views.ViewPurchaseComplete, name='purchaseComplete'),
    # 取引
    path('transaction/<uuid:id>', views.ViewTransaction, name='transaction'),
    path('transactionShipped/<uuid:id>', views.ViewTransactionShipped, name='transactionShipped'),
    path('transactionArrived/<uuid:id>', views.ViewTransactionArrived, name='transactionArrived'),
    
    # 
    # 一覧
    # 
    # いいね一覧
    path('favorite/', views.ViewListFavorite.as_view(), name='favoriteList'),
    # 出品一覧
    path('sellList/', views.ViewListSell.as_view(), name='sellList'),
    # 購入一覧
    path('buyList/', views.ViewListBuy.as_view(), name='buyList'),
]
if settings.DEBUG:
    urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)