from django.contrib.auth.models import Group, User
from django.db import models
from rest_framework import serializers

class Family(Group):
    family_name = models.CharField(max_length=200, unique=True)
    personal = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_families')

    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Families"
        ordering = ['name']

    def __unicode__(self):
        return self.name
    
    def user_is_owner(self, user: User):
        return user.owned_families.filter(id=self.id).exists()
    
    def is_user_part(self, user: User):
        return user.groups.filter(id=self.id).exists()

class FamilySerialize(serializers.ModelSerializer):
    familyName = serializers.CharField(source='family_name')

    class Meta:
        model = Family
        fields = ['id', 'name', 'familyName', 'personal']
