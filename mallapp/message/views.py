from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from item.models import Item
from .models import Conversation
from .forms import ConversationForm

@login_required
def new_conversation(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')

    # Check if the requester is in the member list
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        pass # redirect it to post

    if request.method == 'POST':
        form = ConversationForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.post = conversation
            conversation_message.created_by = request.user
            # if id is not provided, it will lead to a not-null error(absence of message id)
            conversation_message.message_id = conversation.id
            conversation_message.save()

            return redirect('item:detail', pk=pk)
    else:
        form = ConversationForm()

    return render(request, 'message/newpost.html',{
        'form':form
    })

@login_required
def inbox(request):
    # Check if the requester is in the member list
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'message/inbox.html',{
        'conversations':conversations
    })

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    return render(request, 'message/inbox.html',{
        'conversation':conversation
    })