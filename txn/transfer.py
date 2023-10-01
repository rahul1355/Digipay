from django.shortcuts import render,redirect
from bankaccounts.models import Account,KYC
from django.db.models import Q  
from django.contrib import messages
from transaction.models import Transaction


# Create your views here.
def search_user_by_account_number(request):
    account = Account.objects.all()
    
    query = request.POST.get("account_number")
    
    if query:
        account = account.filter(
            Q(account_number=query)
        ).distinct()
    
    context = {
        "account": account,
        "query":query
    }
    return render(request,"transaction/search-user-by-account-number.html",context)

def amount_transfer(request,account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request,"Account doesn't exist")
        return redirect('search')
    
    context = {
        'account':account
    }
    return render(request,"transaction/amount-transfer.html",context)

def Amount_transfer_process(request,account_number):
    account = Account.objects.get(account_number=account_number) # Get the account from which you need send the amount
    
    sender = request.user # get the person who is logged in
    reciever = account.user # get the person to whom you need to send the amount or the person who receive the amount

    sender_account = request.user.account ## get the currently logged in users account that would send the money
    reciever_account = account # get the the person account that would receive the money

    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")

        print(amount)
        print(description)
        
        if sender_account.account_balance > 0 and amount:
            new_transaction = Transaction.objects.create(
                user = request.user,
                amount = amount,
                description = description,
                sender_account = sender_account,
                sender = sender,
                reciever = reciever,
                reciever_account = reciever_account,
                status = "processing",
                transaction_type = "None"
            )
            new_transaction.save()
            
            transaction_id = new_transaction.transaction_id
        
            return redirect("transfer-confirmation",account.account_number, transaction_id)
        else:
            messages.warning(request, "Insufficient Fund.")
            return redirect("amount-transfer", account.account_number)

    return render(request,"transaction/amount-transfer-process.html",{})

def transfer_confirmation(request,account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        'account':account,
        'transaction':transaction   
    }
    return render(request,"transaction/transfer-confirmation.html",context)

def transfer_process(request,account_number,transaction_id):
    pass
    
def transfer_completed(request,account_number,transaction_id):
    return render(request,"transaction/transfer-completed.html",{})
                
    