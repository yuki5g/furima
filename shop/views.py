from datetime import datetime
from urllib import request, response
from numpy import var
from .models import (
    ModelItemList,
    ModelListStatus,
    ModelShipStatus,
    ModelTransactionStatus
)
from .form import (
    userCreateForm,
    userUpdateForm,
    itemForm,
    passwordChangeForm,
    passwordResetForm,
)
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView
)
from django.contrib.auth import (
     get_user_model,
     login as auth_login,
     logout as auth_logout
)
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from django.core.paginator import(
    Paginator,
    EmptyPage,
    PageNotAnInteger
)

User = get_user_model()
# 
# トップページ
# 
class ViewItemList(ListView):
    """トップページ"""
    model = ModelItemList
    template_name = 'shop/TempTop.html'
    paginate_by = 9

    # 一覧表示、検索機能
    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word:
            object_list = ModelItemList.objects.filter(
                Q(name__icontains=q_word)).order_by('-lastUpdate')
        else:
            object_list = ModelItemList.objects.all().order_by('-lastUpdate')
        return object_list

# 
# 商品情報
# 
def ViewCreateItem(request):
    """商品情報登録"""
    if request.method == 'POST':
        varForm = itemForm(request.POST or None,request.FILES)
        if varForm.is_valid():
            list = ModelItemList()
            list.image1 = varForm.cleaned_data['image1']
            list.name = varForm.cleaned_data['name']
            list.price = varForm.cleaned_data['price']
            list.category = varForm.cleaned_data['category']
            list.status = varForm.cleaned_data['status']
            list.description = varForm.cleaned_data['description']
            list.bearShippingFee = varForm.cleaned_data['bearShippingFee']
            list.shippingFee = varForm.cleaned_data['shippingFee']
            list.shippingMethod = varForm.cleaned_data['shippingMethod']
            list.shipArea = varForm.cleaned_data['shipArea']
            list.shippingTime = varForm.cleaned_data['shippingTime']

            ModelItemList.objects.create(
                # id = list.id,
                image1 = list.image1,
                name = list.name,
                price = list.price,
                category = list.category,
                status = list.status,
                description = list.description,
                bearShippingFee = list.bearShippingFee,
                shippingFee = list.shippingFee,
                shippingMethod = list.shippingMethod,
                shipArea = list.shipArea,
                shippingTime = list.shippingTime,
                seller = request.user,
                sellDate = datetime.now(),
                lastUpdate = datetime.now()
            )
            messages.success(request, '商品を出品しました。')
            return redirect('shop:top')
    else:
        varForm = itemForm()
        context = {
            'form': varForm
        }
    return render(request, 'shop/TempCreateItem.html', context)
    
def ViewReadItem(request, id):
    """商品情報詳細"""
    varItem = get_object_or_404(ModelItemList, pk=id)
    context = {
        'item': varItem
    }
    return render(request,
                  'shop/TempReadItem.html', context)

def ViewUpdateItem(request, id):
    """商品情報編集"""
    varItem = get_object_or_404(ModelItemList, pk=id)
    varForm = itemForm(instance=varItem)
    context = {
        'item':varItem,
        'form':varForm,
    }
    return render(request, 'shop/TempUpdateItem.html', context)

def ViewUpdateItemComplete(request,id):
    """商品情報編集 完了"""
    if request.method == 'POST':
        varItem = get_object_or_404(ModelItemList,pk=id)
        varForm = itemForm(request.POST,instance=varItem)
        if varForm.is_valid():
            varForm.save()
    messages.success(request, '商品情報を更新しました。')
    return redirect('shop:readItem', id=id)

def ViewDeleteItem(request,id):
    """商品情報削除"""
    varItem = get_object_or_404(ModelItemList,pk=id)
    varItem.delete()
    messages.warning(request, '商品情報を削除しました。')
    return redirect('shop:top')

# 
# 利用者情報
# 
class SignUpView(generic.CreateView):
    """利用者情報登録"""
    form_class = userCreateForm
    success_url = reverse_lazy('login')
    template_name = 'shop/TempCreateUser.html'
    def form_valid(self, form):
        user = form.save() # formの情報を保存
        auth_login(self.request, user) # 認証
        self.object = user
        messages.success(self.request, 'ユーザー登録が完了しました。ようこそ')
        return redirect('shop:top')

def ViewReadUser(request,id):
    """利用者情報詳細"""
    varUser = get_object_or_404(User, pk=id)
    verItem = ModelItemList.objects.filter(seller=id).order_by('-id')
    context = {
        'user': varUser,
        'item': verItem,
    }
    return render(request, 'shop/TempReadUser.html', context) 

def ViewUpdateUser(request):
    """利用者情報更新"""
    varUser = get_object_or_404(User, pk=request.user.id)
    verForm = userUpdateForm(instance=varUser)

    context = {
        'user':varUser,
        'form':verForm,
    }
    return render(request, 'shop/TempUpdateUser.html', context)

def ViewUpdateUserComplete(request):
    """利用者情報更新 完了"""
    if request.method == 'POST':
        varUser = get_object_or_404(User,pk=request.user.id)
        varForm = userUpdateForm(request.POST,instance=varUser)
        varForm.save()
        messages.success(request, 'ユーザ情報を更新しました。')
    return redirect('shop:mypage')

class DeleteView(LoginRequiredMixin, generic.View):
    """利用者情報削除"""
    def get(self, *args, **kwargs):
        varUser = User.objects.get(email=self.request.user.email)
        varUser.is_active = False
        varUser.save()
        auth_logout(self.request)
        messages.warning(self.request, '退会しました。ご利用いただきありがとうございました。')
        return redirect('shop:top')

# 
# ログイン / ログアウト / マイページ
# 
class Logout(LoginRequiredMixin, LogoutView):
    """ログアウト"""
    template_name = 'shop/TempLogout.html'

class ProfileView(LoginRequiredMixin, generic.View):
    """マイページ"""
    def get(self, *args, **kwargs):
        return render(self.request,'shop/TempMypage.html')

# 
# パスワード
# 
class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = passwordChangeForm
    success_url = reverse_lazy('shop:passwordChangeDone')
    template_name = 'shop/TempPasswordChange.html'

class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'shop/TempPasswordChangeDone.html'

# 1.パスワードリセットページでメールアドレスを入力
class passwordResetForm(PasswordResetView):
    """パスワードリセットフォーム"""
    form_class = passwordResetForm
    template_name = 'shop/TempPasswordResetForm.html'
    from_email = 'yuki700g@gmail.com'
    success_url = reverse_lazy('shop:passwordResetDone')

# 2.メール送信完了ページが表示され、パスワードリセットメールを受信
class passwordResetDone(PasswordResetDoneView):
    """パスワードリセット メール送信完了"""
    template_name = 'shop/TempPasswordResetDone.html'

# 3.メールに記載されているリンクをクリック
class passwordResetEmail(PasswordResetView):
    """パスワードリセットEメール"""
    email_template_name = 'shop/TempPasswordResetEmail.html'
    template_name = 'shop/TempPasswordResetEmail.html'
    from_email = 'yuki700g@gmail.com'
    success_url = reverse_lazy('shop:TempPasswordResetDone')


# 4.パスワード更新ページから新パスワードを設定
class passwordResetConfirm(PasswordResetConfirmView):
    """パスワードリセット確認"""
    template_name = 'shop/TempPasswordResetConfirm.html'

# 5.パスワード更新完了ページが表示
class passwordResetComplete(PasswordResetCompleteView):
    """パスワードリセット完了"""
    template_name = 'shop/TempPasswordResetComplete.html'

# 
# 商品取引
# 
def ViewPurchase(request, id):
    """商品購入"""
    varItem = get_object_or_404(ModelItemList, pk=id)
    context = {
        'item': varItem
    }
    return render(request,
                  'shop/TempPurchase.html', context)

def ViewPurchaseComplete(request, id):
    """商品購入処理"""
    # レコード作成・更新用のモデルクラスインスタンスを作成
    varItem = ModelItemList.objects.get(pk = id)
    varSeller = varItem.seller
    varTransactionStatusStartTransaction = ModelTransactionStatus.objects.get(id = 1)
    varShipStatusUnsent = ModelShipStatus.objects.get(id = 0)
    varListStatusUnselling = ModelListStatus.objects.get(id = 1)

    # 商品レコードを更新
    varItem.lastUpdate = datetime.now()
    varItem.buyer = request.user
    varItem.seller = varSeller
    varItem.listStatus = varListStatusUnselling
    varItem.transactionStatus = varTransactionStatusStartTransaction
    varItem.shipStatus = varShipStatusUnsent
    varItem.transactionStartDate = datetime.now()
    varItem.save()

    messages.success(request, '商品を購入しました。')
    return redirect('shop:readItem', id = varItem.id)

def ViewTransaction(request, id):
    """取引"""
    varItem = get_object_or_404(ModelItemList, pk=id)
    context = {
        'item':varItem,
    }
    return render(request, 'shop/TempTransaction.html', context)

def ViewTransactionShipped(request,id):
    """取引 発送済み"""
    varTransactionStatusShipped = ModelTransactionStatus.objects.get(id=2)
    varShipStatusShipping = ModelShipStatus.objects.get(id=2)

    # 商品レコードを更新
    varItem = ModelItemList.objects.get(pk=id)
    varItem.transactionStatus = varTransactionStatusShipped
    varItem.shipStatus = varShipStatusShipping
    varItem.lastUpdate = datetime.now()
    varItem.save()

    messages.success(request, '発送連絡をしました。')
    return redirect('shop:transaction', id)

def ViewTransactionArrived(request,id):
    """取引 受け取り完了"""
    varTransactionComplete = ModelTransactionStatus.objects.get(id=3)
    varShipStatusArrived = ModelShipStatus.objects.get(id=3)

    # 商品レコードを更新
    varItem = ModelItemList.objects.get(pk=id)
    varItem.transactionStatus = varTransactionComplete
    varItem.shipStatus = varShipStatusArrived
    varItem.lastUpdate = datetime.now()
    varItem.save()

    messages.success(request, '受け取り連絡をしました。')
    return redirect('shop:transaction', id)

# 
# 一覧
# 
class ViewListFavorite(LoginRequiredMixin, ListView):
    """お気に入りリスト"""
    template_name = 'shop/TempListFavorite.html'
    def get_queryset(self):
        return ModelItemList.objects.filter(seller = self.request.user).order_by('-lastUpdate')

class ViewListSell(LoginRequiredMixin, ListView):
    """出品リスト"""
    template_name = 'shop/TempListSell.html'
    def get_queryset(self):
        return ModelItemList.objects.filter(seller = self.request.user).order_by('-lastUpdate')

class ViewListBuy(LoginRequiredMixin, ListView):
    """購入リスト"""
    template_name = 'shop/TempListBuy.html'
    def get_queryset(self):
        return ModelItemList.objects.filter(buyer = self.request.user).order_by('-lastUpdate')