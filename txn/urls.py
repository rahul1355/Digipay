from django.urls import path 
from transaction import views 
from transaction import transfer

app_name = 'transaction'

urlpatterns = [
    path('',transfer.search_user_by_account_number,name="search"),
    path('amount-transfer/<account_number>/',transfer.amount_transfer,name="amount-transfer"),
    path("amount-transfer-process/<account_number>/", transfer.Amount_transfer_process, name="amount-transfer-process"),
    path("transfer-confirmation/<account_number>/<transaction_id>/",transfer.transfer_confirmation,name="transfer-confirmation")
]
