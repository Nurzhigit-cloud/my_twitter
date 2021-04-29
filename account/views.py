from django.db.models import Q
from django.views import View

from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView



from django.shortcuts import render




def registration_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'post_list.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/registration.html', {'user_form': user_form})


class UserLoginView(LoginView):
    # form_class = AuthUserFrom
    template_name = 'account/login.html'
    success_url = reverse_lazy('post_list')



class ProfileUserView(TemplateView):
    template_name = "account/profile.html"


# class SearchResultsView(View):
#     def get(self, request):
#         search_param = request.GET.get('q')
#         results = Product.objects.filter(Q(title__icontains=search_param) | Q(description__icontains=search_param))
#
#         # select * from product where title ilike ' '  or description ilike ' '
#         return render(request, 'product/search_results.html', locals())


