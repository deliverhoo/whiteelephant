from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Game, Player, Gift, GameProperties
from .serializers import GameSerializer, PlayerSerializer, GiftSerializer, GamePropertiesSerializer, GiftSummarySerializer
import random

def summary_page(request,game_id):
    gifts = Gift.objects.filter(game=game_id)
    context= {
        'gifts':GiftSummarySerializer(gifts, many=True).data
    }
    return render(request, 'summary.html', context)


def index(request):
    games = Game.objects.all()
    searializer = GameSerializer(games, many=True)
    print(searializer.data)
    context = {'games':searializer.data}
    return render(request, 'index.html', context)

def game_page(request,game_id):
    game = Game.objects.get(pk=game_id)
    properties = GameProperties.objects.get(game=game)
    players= Player.objects.filter(game=game)
    gifts = Gift.objects.filter(game=game)
    unopened_gifts = Gift.objects.filter(game=game, current_owner=None, )
    unopened_gifts = unopened_gifts.order_by('?')
    
    #print(PlayerSerializer(players,many=True).data)
    gif_num = str(random.randint(1,15))
    context = {
        'game': GameSerializer(game,many=False).data,
        'properties': GamePropertiesSerializer(properties, many=False).data,
        'players': PlayerSerializer(players,many=True).data,
        'gifts': GiftSerializer(gifts, many=True).data,
        'unopened_gifts': GiftSerializer(unopened_gifts, many=True).data,
        'gif_num':gif_num,
    }
    return render(request, 'game.html', context)

#----------------POST METHODS-------------------------------
#We will still use GET, but it will modify database state
#not a good idea but its easy for now
@csrf_exempt
@api_view(['GET'])
def start_game(request,game_id):
    game=None
    game_properties=None
    game_players=None
    gifts=None
    try:
        game = Game.objects.get(pk=game_id)
        properties = GameProperties.objects.get(game=game)
        players= Player.objects.filter(game=game)
        gifts = Gift.objects.filter(game=game)

        #can start game if game has not already started
        if properties.started is False:
            #initialize position for all players and save current player and next position
            number_of_players = len(players)
            #list of positions
            list_position = []
            for i in range(1,number_of_players+1):
                list_position.append(i)
            random.shuffle(list_position)

            for i in range(0,number_of_players):
                players[i].position = list_position[i]
                players[i].save()

                #save game properties for position 1 and 2
                if list_position[i] == 1:
                    properties.current_player = players[i]
                    properties.next_position = 2
                    properties.started = True
                    properties.save()
    except Exception as e:
        print(e)
        #any kinf of error, return not found. Game will have to be reset
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    searializer = GameSerializer(game, many=False)
    return Response(searializer.data)


@csrf_exempt
@api_view(['GET']) 
def reset_game(request,game_id):
    game=None
    game_properties=None
    game_players=None
    gifts=None
    try:
        game = Game.objects.get(pk=game_id)
        properties = GameProperties.objects.get(game=game)
        players= Player.objects.filter(game=game)
        gifts = Gift.objects.filter(game=game)

        #reset position for all players
        for p in players:
            p.position = 0
            p.save()
        
        #reset gift stolen and gift locked value
        for g in gifts:
            g.locked = False
            g.current_owner = None
            g.number_of_times_stolen = 0
            g.save()
        
        properties.current_player = None
        properties.next_position = 0
        properties.no_lock_stage=False
        properties.started=False
        properties.ended=False
        properties.save()

    except:
        #any kinf of error, return not found. Dont know what to do
        #in prod, should never get here.
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    searializer = GameSerializer(game, many=False)
    return Response(searializer.data)

@csrf_exempt
@api_view(['GET'])
def open_gift(request,game_id,gift_id):
    properties = None
    try:
        game = Game.objects.get(pk=game_id)
        gift = Gift.objects.get(pk=gift_id, game=game)
        properties = GameProperties.objects.get(game=game)
        
        #perforn sanity checks
        if gift.current_owner is not None:
            raise Exception("Gift is already opened")
        if properties.started == False:
            raise Exception("Game has not started")
        if properties.ended == True:
            raise Exception("Game has already ended")
        if properties.no_lock_stage == True:
            raise Exception("All gifts have been opened already")

        #check if this player already has a gift or not
        all_gifts = Gift.objects.filter(game=game)
        for g in all_gifts:
            if g.current_owner == properties.current_player:
                raise Exception("Player already has a gift. Cant open a new one")
    
        #unlock all gifts since opening a new gift will start a new round
        for g in all_gifts:
            g.locked = False
            g.save()

        #move current owner
        gift.current_owner = properties.current_player
        gift.save()

        #decide new current player and the new next_posiotion
        players = Player.objects.filter(game=game)
        for p in players:
            if properties.next_position == -1 and p.position == 1:
                #that means enter the no lock stage of the game,
                #make player 1 the current plater
                properties.current_player = p
                properties.no_lock_stage = True
                break
            elif p.position == properties.next_position:
                properties.current_player = p
                #if last position, then set position to 1
                if p.position == len(players):
                    properties.next_position = -1
                else:
                    properties.next_position = properties.next_position+1
                #if found next person, then break
                break
        properties.save()
        
        #game cant end by just opening gifts.
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)

    searializer = PlayerSerializer(properties.current_player, many=False)
    return Response(searializer.data) 

@csrf_exempt
@api_view(['GET'])
def steal_gift(request,game_id,gift_id):
    properties=None
    try:
        game = Game.objects.get(pk=game_id)
        gift = Gift.objects.get(pk=gift_id, game=game)
        properties = GameProperties.objects.get(game=game)

        #sanity checks
        if gift.current_owner is None:
            raise Exception("Gift is not yet opened")
        if gift.number_of_times_stolen >= 3:
            raise Exception("Gift already stolen maximum times")
        if gift.locked:
            raise Exception("Gift is locked")
        
        
        if properties.no_lock_stage == True:
            all_gifts = Gift.objects.filter(game=game)
            #unlock all gifts and lock just the currently stolen one
            for g in all_gifts:
                g.locked = False
                g.save()


            to_give_gift = Gift.objects.get(game=game, current_owner = properties.current_player)

            #print(to_give_gift)
            #gift is the gift that needs to be stolen
            new_player = gift.current_owner

            gift.number_of_times_stolen = gift.number_of_times_stolen + 1
            gift.current_owner = properties.current_player
            gift.locked = True
            gift.save()


            to_give_gift.current_owner = new_player
            to_give_gift.save()

            properties.current_player = new_player
            properties.save()

        else:
            #just steal
            old_player = properties.current_player
            #print(old_player.first_name)

            properties.current_player = gift.current_owner
            properties.save()
            
            #print(gift.current_owner)

            #print(old_player.first_name)

            gift.current_owner = old_player
            gift.number_of_times_stolen = gift.number_of_times_stolen+1
            gift.locked = True
            gift.save()

    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)

    searializer = PlayerSerializer(properties.current_player, many=False)
    return Response(searializer.data) 

#in the end, if the last person does not want to swap
#only valid in no lock stage
@csrf_exempt
@api_view(['GET'])
def keep_gift(request,game_id):
    properties = None
    try:
        properties = GameProperties.objects.get(game=game_id)
        properties.current_player = None
        if properties.no_lock_stage != True:
            raise Exception("Not in final stage yet")

        properties.ended = True
        properties.save()

        #release lock from all gifts
        all_gifts = Gift.objects.filter(game=game_id)
        #unlock all gifts and lock just the currently stolen one
        for g in all_gifts:
            g.locked = False
            g.save()

    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)

    searializer = GamePropertiesSerializer(properties, many=False)
    return Response(searializer.data)
#----------------GET METHODS-------------------------------
@csrf_exempt
@api_view(['GET'])
def games_list(request):
    games = Game.objects.all()
    searializer = GameSerializer(games, many=True)
    return Response(searializer.data)


@csrf_exempt
@api_view(['GET'])
def get_all_players(request,game_id):
    for_game = None
    try:
        for_game = Game.objects.get(pk=game_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    players = Player.objects.filter(game = for_game)
    searializer = PlayerSerializer(players, many=True)
    return Response(searializer.data)


@csrf_exempt
@api_view(['GET'])
def get_current_player(request,game_id):
    game_prop = None
    player = None
    try:
        game_prop = GameProperties.objects.get(game=game_id)
        player = game_prop.current_player
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    searializer = PlayerSerializer(player, many=False)
    return Response(searializer.data)


@csrf_exempt
@api_view(['GET'])
def get_unopened_gifts(request,game_id):
    gifts = None
    try:
        game = Game.objects.get(pk=game_id)
        gifts = Gift.objects.filter(game=game, current_owner=None)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    searializer = GiftSerializer(gifts, many=True)
    return Response(searializer.data)

@csrf_exempt
@api_view(['GET'])
def get_all_gifts(request,game_id):
    gifts = None
    try:
        game = Game.objects.get(pk=game_id)
        gifts = Gift.objects.filter(game=game)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    searializer = GiftSerializer(gifts, many=True)
    return Response(searializer.data)

@csrf_exempt
@api_view(['GET'])
def get_game_properties(request,game_id):
    props = None
    try:
        game = Game.objects.get(pk=game_id)
        props = GameProperties.objects.get(game=game)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    searializer = GamePropertiesSerializer(props, many=False)
    return Response(searializer.data)