from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Acount(models.Model): # acount esta vinculado con lo usuario de django
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    email = models.EmailField(unique=True) # se inicia sesion con el email
    
    name = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    date = models.DateField() # fecha de nacimiento    
    phone = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.id}, {self.email}, {self.password}, {self.name}, {self.lastName}, {self.date}, {self.phone}"
    
'''    @staticmethod
    def exist(email, password): # borrar metodo no se si lo llegue a implementar
        try:
            user = Acount.objects.get(email=email, password=password)
            return user
        except Acount.DoesNotExist:
            return None
        
'''






    