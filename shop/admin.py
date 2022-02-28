from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import (
    User,
    ModelArea,
    ModelShippingTime,
    ModelBearShippingFee,
    ModelItemCategory,
    ModelItemCategoryDetail,
    ModelItemCondition,
    ModelItemList,
    ModelShippingMethod
)

admin.site.register(User)
admin.site.register(ModelArea)
admin.site.register(ModelShippingTime)
admin.site.register(ModelBearShippingFee)
admin.site.register(ModelItemCategory)
admin.site.register(ModelItemCategoryDetail)
admin.site.register(ModelItemCondition)
admin.site.register(ModelItemList)
admin.site.register(ModelShippingMethod)