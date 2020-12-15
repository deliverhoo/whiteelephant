from rest_framework import serializers
from .models import Game, Player, Gift, GameProperties

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Game
        fields='__all__'
    
class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model=Gift
        fields='__all__'

class PlayerSerializer(serializers.ModelSerializer):
    current_gift = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    class Meta:
        model=Player
        fields=['game','first_name','last_name','photo_name','position','current_gift', 'is_active']

    def get_current_gift(self,obj):
        cg = None
        try:
            cg = Gift.objects.get(current_owner=obj.pk, game=obj.game)
        except:
            #if current owner does not have a gift
            cg=None
        return GiftSerializer(cg, many=False).data

    def get_is_active(self,obj):
        if (GameProperties.objects.get(game=obj.game).current_player == obj):
            return True
        else:
            return False


class GamePropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameProperties
        fields = '__all__'


class SimplePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Player
        fields=['first_name','last_name']

class GiftSummarySerializer(serializers.ModelSerializer):
    original_owner = SimplePlayerSerializer(many=False, read_only=True)
    current_owner = SimplePlayerSerializer(many=False, read_only=True)

    class Meta:
        model=Gift
        fields=['file_name','original_owner','current_owner']