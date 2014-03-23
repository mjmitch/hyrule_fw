from django.contrib import admin
from models import Player, Character, CharacterClass, Rank

class CharacterInline(admin.StackedInline):
    model = Character
    extra = 0

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Info', {'fields': ['rank', 'approved']}),
        ('Adv.', {'fields': {'user'}})
    ]
    inlines = [CharacterInline]


class CharacterClassAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Image', {'fields': ['image']})
    ]


class CharacterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'player']}),
        ('Info', {'fields': ['level', 'character_class', 'is_main']})
    ]
    readonly_fields = ['is_main']


class RankAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Permissions', {'fields': ['default', 'officer_perms', 'admin_perms']})
    ]
    readonly_fields = ['default']

admin.site.register(Character, CharacterAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(CharacterClass, CharacterClassAdmin)
admin.site.register(Rank, RankAdmin)