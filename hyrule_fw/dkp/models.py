from django.db import models

#START: Player Models

class Rank(models.Model):
    name = models.CharField(max_length=24)
    officer_perms = models.BooleanField(default=False)
    admin_perms = models.BooleanField(default=False)
    default = models.BooleanField(default=False)

class CharacterClass(models.Model):
    name = models.CharField(max_length=24)
    image = models.ImageField(upload_to='images/character_classes')

class TalentTreeType(models.Model):
    name = models.CharField(max_length=24)
    character_class = models.ForeignKey(CharacterClass)

class TalentType(models.Model):
    name = models.CharField(max_length=24)
    talent_tree_type = models.ForeignKey(TalentTreeType)
    character_class = models.ForeignKey(CharacterClass, blank=True)
    description = models.TextField()
    max_points = models.PositiveSmallIntegerField()
    has_rune = models.BooleanField(default=False)
    required_points = models.PositiveIntegerField()
    x_position = models.PositiveSmallIntegerField(help_text='Left-Most position is Position #1 (Right-Most is #4)')
    has_parent = models.BooleanField(default=False)
    parent_id = models.PositiveIntegerField(blank=True)
    parent_requirements = models.PositiveSmallIntegerField(default=0, help_text='How many points does the parent ' +
                                                                                'talent need to have to activate ' +
                                                                                'this talent? Leave value at "0" if ' +
                                                                                'there is no parent talent.')

    def find_parent(self):
        potentials = []
        closest_points = self.required_points
        closest = None
        for talent in self.talent_tree_type.talenttype_set.all():
            if self.x_position == talent.x_position and self.required_points > talent.required_points:
                dist = self.required_points - talent.required_points
                if dist < closest_points:
                    closest_points = dist
                    closest = talent.id
        return closest

    def save(self, *args, **kwargs):
        if self.has_parent and not self.parent_id:
            self.parent_id = self.find_parent()
        self.character_class = self.talent_tree_type.character_class
        super(TalentType, self).save(*args, **kwargs)

class Talent(models.Model):
    name = models.CharField(max_length=24, blank=True)
    talent_type = models.ForeignKey(TalentType)
    points = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.points > self.talent_type.max_points:
            self.points = self.talent_type.max_points
        super(Talent, self).save(*args, **kwargs)

class TalentTree(models.Model):
    name = models.CharField(max_length=60, blank=True)
    talent_tree_type = models.ForeignKey(TalentTreeType)

class Player(models.Model):
    name = models.CharField(max_length=40)
    main = models.ForeignKey(Character)
    rank = models.ForeignKey(Rank, blank=True)

    def save(self, *args, **kwargs):
        self.main.is_main = True
        if not self.rank:
            self.rank = Rank.objects.get(default=True)
        super(Player, self).save(*args, **kwargs)

class Character(models.Model):
    name = models.CharField(max_length=40)
    character_class = models.ForeignKey(CharacterClass)
    talent_tree = models.ForeignKey(TalentTree, blank=True)
    talent_tree_2 = models.ForeignKey(TalentTree, blank=True)
    player = models.ForeignKey(Player)
    is_main = models.BooleanField(default=False)
    level = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        if self.level > 80:
            self.level = 80
        super(Character, self).save(*args, **kwargs)
# END: Player Models
# START: Shop Models

class ItemType(models.Model):
    name = models.CharField(max_length=40)
    default_image = models.ImageField(upload_to='images/item_types')

class Category(models.Model):
    name = models.CharField(max_length=40)
    description =  models.TextField(blank=True)
    active = models.BooleanField(blank=True, default=True)

BASE_ATTRIBUTES_1 = {
    'Attack': 'Attack',
    'Defense': 'Defense',
    }
BASE_ATTRIBUTES_2 = {
    'Health': 'Health',
    'Mana': 'Mana',
    }
class GearType(ItemType):
    type = models.CharField(max_length=10, help_text='Head, Chest, Weapon, etc...')
    base_attribute_1 = models.CharField(max_length=7, choices=BASE_ATTRIBUTES_1)
    base_attribute_1_value = models.PositiveIntegerField()
    base_attribute_2 = models.CharField(max_length=6, choices=BASE_ATTRIBUTES_2)
    base_attribute_2_value = models.PositiveIntegerField()

class Item(models.Model):
    name = models.CharField(max_length=64)
    dkp_cost = models.PositiveIntegerField()
    quantity_in_stock = models.PositiveIntegerField()
    active = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.quantity_in_stock:
            self.active = True
        else:
            self.active = False
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

class GearItem(Item):
    gear_type = models.ForeignKey(GearType)
    character_class = models.ForeignKey(CharacterClass)
    can_reforge = models.BooleanField(default=False)
    owner = models.ForeignKey(Character, blank=True)
    fortify_level = models.CharField(choices=({i:i} for i in range(13)), blank=True)
    
    def save(self, *args, **kwargs):
        if not self.fortify_level:
            self.fortify_level = 0
        super(GearItem, self).save(*args, **kwargs)

class Attribute(models.Model):
    name = models.CharField(max_length=32, help_text="Attack, Crit Chance, etc...")
    value = models.CharField(max_length=4, help_text='Include the % sign if it is a percent (Crit chance, for example)')

class AdditionalAttribute(Attribute):
    gear_item = models.ForeignKey(GearItem)

class IdentifiedAttribute(Attribute):
    gear_item = models.ForeignKey(GearItem)

class LegendaryAttribute(Attribute):
    gear_item = models.ForeignKey(GearItem)

class Cart(models.Model):
    player = models.ForeignKey(Player)
    total_dkp_cost = models.PositiveIntegerField(blank=True)
    has_items = models.BooleanField(blank=True, default=False)
    
    def save(self, *args, **kwargs):
        if self.cartitem_set.count():
            self.has_items = True
        super(Cart, self).save(*args, **kwargs)

class CartItem(models.Model):
    item = models.ForeignKey(Item)
    quantity = models.PositiveIntegerField(blank=True)
    cart = models.ForeignKey(Cart)
    processed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.quantity:
            self.quantity = 1
        super(CartItem, self).save(*args, **kwargs)

# END: Shop Models
# START: Event Models

class EventType(models.Model):
    name = models.CharField(max_length=64)
    default_dkp_reward = models.PositiveIntegerField(blank=True)
    image = models.ImageField(upload_to='images/events', blank=True)

class Event(models.Model):
    event_type = models.ForeignKey(EventType)
    start_date = models.DateField()
    start_time = models.TimeField()
    dkp = models.PositiveIntegerField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.dkp and self.event_type.default_dkp_reward:
            self.dkp = self.event_type.default_dkp_reward
        super(Event, self).save(*args, **kwargs)