from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View

from chat.forms import ChannelForm
from chat.models import ChatType


class CreateChannelView(View):
    def get(self, request):
        form = ChannelForm(user=request.user)
        return render(request, 'chat/create_channel.html', {'form': form})

    def post(self, request):
        form = ChannelForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.creator = request.user
            channel.chat_type = ChatType.CHANNEL.name
            channel.save()
            form.save_m2m()
            channel.users.add(request.user)
            return redirect(reverse('room_view', args=[str(channel.id)]))
        return render(request, 'chat/create_channel.html', {'form': form})
