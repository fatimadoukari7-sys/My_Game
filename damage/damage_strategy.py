from abc import ABC, abstractmethod


class DamageStrategy(ABC):

    @abstractmethod
    def calculate_damage(self, attack):
        pass
class NormalDamage(DamageStrategy):

    def calculate_damage(self, attack):
        return attack
class ResistantDamage(DamageStrategy):

    def calculate_damage(self, attack):
        return max(0, attack - 1)

class DoubleDamage(DamageStrategy):

    def calculate_damage(self, attack):
        return attack * 2    
