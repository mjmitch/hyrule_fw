from django.db import models

from hyrule_fw.players.models import Player, CharacterClass, Character


class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    active = models.BooleanField(blank=True, default=True)


class GearType(models.Model):
    class Meta:
        verbose_name = "Gear Type"

    name = models.CharField(max_length=10, help_text='Head, Chest, Weapon, etc...')


class Item(models.Model):
    name = models.CharField(max_length=64)
    cost = models.PositiveIntegerField()
    quantity_in_stock = models.PositiveIntegerField(blank=True)
    active = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)

    def save(self, *args, **kwargs):
        self.active = self.quantity_in_stock > 0
        super(Item, self).save(*args, **kwargs)

RUNE_ENERGY_TYPES = {
    'Wisdom': 'Wisdom',
    'Fervor': 'Fervor',
    'Nature': 'Nature',
}


class Rune(Item):
    character_class = models.ForeignKey(CharacterClass)
    skill_name = models.CharField(max_length=32)
    energy_type = models.CharField(max_length=8, choices=RUNE_ENERGY_TYPES)
    energy_value = models.PositiveIntegerField()


class Scroll(Item):
    skill_name = models.CharField(max_length=32)
    skill_level = models.PositiveIntegerField()
    character_class = models.ForeignKey(CharacterClass)


class GearItem(Item):
    class Meta:
        verbose_name = "Gear Item"

    gear_type = models.ForeignKey(GearType)
    character_class = models.ForeignKey(CharacterClass)
    can_reforge = models.BooleanField(default=False)
    owner = models.ForeignKey(Character, blank=True)
    fortify_level = models.CharField(choices=({i: i} for i in range(13)), blank=True)
    
    def save(self, *args, **kwargs):
        if not self.fortify_level:
            self.fortify_level = 0
        super(GearItem, self).save(*args, **kwargs)


class Attribute(models.Model):
    name = models.CharField(max_length=32, help_text="Attack, Crit Chance, etc...")
    value = models.CharField(max_length=4, help_text='Include the % sign if it is a percent (Crit chance, for example)')
    gear_item = models.ForeignKey(GearItem)

class BaseAttribute(Attribute):
    class Meta:
        verbose_name = "Base Attribute"

class AdditionalAttribute(Attribute):
    class Meta:
        verbose_name = "Additional Attribute"


class IdentifiedAttribute(Attribute):
    class Meta:
        verbose_name = "Identified Attribute"


class LegendaryAttribute(Attribute):
    class Meta:
        verbose_name = "Legendary Attribute"


class Cart(models.Model):
    player = models.ForeignKey(Player)
    total_cost = models.PositiveIntegerField(blank=True)
    has_items = models.BooleanField(blank=True, default=False)

    def save(self, *args, **kwargs):
        self.has_items = False
        if self.cartitem_set.count():
            for cart_item in self.cartitem_set.all():
                if not cart_item.hidden:
                    self.has_items = True
        super(Cart, self).save(*args, **kwargs)


class CartItem(models.Model):
    class Meta:
        verbose_name = "Cart Item"

    item = models.ForeignKey(Item)
    quantity = models.IntegerField(blank=True)
    cost = models.PositiveIntegerField(default=0, blank=True)
    cart = models.ForeignKey(Cart, blank=True)
    old_cart_id = models.PositiveSmallIntegerField(blank=True)
    buyer = models.ForeignKey(Player, blank=True)
    purchased = models.BooleanField(default=False)
    mailed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.cost = self.quantity * self.item.dkp_cost
        super(CartItem, self).save(*args, **kwargs)
        if self.cart:
            self.old_cart_id = self.cart.id
            super(CartItem, self).save(*args, **kwargs)
            self.cart.save()
        else:
            if self.old_cart_id:
                Cart.objects.get(id=self.old_cart_id).save()
                self.old_cart_id = None
                super(CartItem, self).save(*args, **kwargs)
            if not self.buyer and not self.purchased:
                self.delete()