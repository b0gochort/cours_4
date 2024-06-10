# models.py
from django.db import models

class KeyPair(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем поле id
    p = models.CharField(max_length=255)
    q = models.CharField(max_length=255)
    g = models.CharField(max_length=255)
    y = models.CharField(max_length=255)

    class Meta:
        app_label = 'auth'

    def __str__(self):
        return f"KeyPair - ID: {self.id}, p: {self.p}, q: {self.q}, g: {self.g}, y: {self.y}"
