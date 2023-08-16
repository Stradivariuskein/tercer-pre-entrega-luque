from apps.login.models import Acount
from apps.agenda.models import Turn
from apps.agenda.forms import SearchForm

def valid_acount(request):
    if request.user.is_authenticated:
        try:
            user = Acount.objects.get(user_id=request.user) # Suponiendo que tienes una relación OneToOneField llamada 'acount' en tu modelo User
        except Acount.DoesNotExist:
            return False
    else:
        return False
    return True

def search_turn(request):
    form = SearchForm(request.GET)
    turns = Turn.objects.all()

    if form.is_valid():
        day_of_week = form.cleaned_data['day_of_week']
        date = form.cleaned_data['date']

        if day_of_week:
            turns = turns.filter(date__week_day=SearchForm.day_choices.index(day_of_week))

        if date:
            turns = turns.filter(date=date)

    return turns
