from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.models import MasterData, PortionData, AlternateName, FoodonId, ReferenceData
from app.serializers import MasterDataSerializer, PortionDataSerializer, AlternateNameSerializer, FoodonIdSerializer, ReferenceDataSerializer
from datetime import datetime
# Create your views here.



@api_view(['GET'])
def ingredient_from_foodon(request, id):
    if request.method == 'GET':
        try:
            ingredient = FoodonId.objects.filter(foodon_id=id).first()
        except FoodonId.DoesNotExist:
            return Response(data={"message": "there is no item with this foodon id!"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = FoodonIdSerializer(ingredient)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ingredients_with_foodons(request):
    """
    Retrieve all ingredients with Foodon IDs and Alternate Names.
    """
    if request.method == 'GET':
        try:
            response_data = []
            all_ingredients = MasterData.objects.all()
            for ingredient in all_ingredients:
                foodons = FoodonId.objects.filter(
                    food_name=ingredient.food_name)
                alternates = AlternateName.objects.filter(food_name=ingredient.food_name)
                response_data.append({"ingredient": ingredient.food_name, "foodon_ids": map(
                    lambda x: x.foodon_id, foodons), "alternate_names": map(lambda x: x.alternate_name, alternates)})
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(repr(e))
            return Response(data={"message": "there was something wrong!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ingredient_data(request):
    if request.method == 'GET':
        name = request.GET.get('ingredient', None)
        try:
            master_object = MasterData.objects.get(food_name=name)
        except ObjectDoesNotExist:
            ingredient_name = AlternateName.objects.get(alternate_name=name)
            master_object = ingredient_name.food_id
        try:
            current_month = datetime.now().month
            reference_data = master_object.best_match_id
            # TODO: add seasonality multiplier here
            # season_info = SeasonalityData.objects.filter(
                # food_id=master_object.id).get(month=current_month)
            # return Response({"Ingredient": master_object.food_name,
            #                 "GHG": master_object.ghg,
            #                 "Season Harvest Data": season_info.harvest,
            #                 "Season Storage Data": season_info.storage},
            #                 status=status.HTTP_200_OK)

            return Response({"ingredient": master_object.food_name, "ghg": reference_data.ghg_global}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": repr(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def portion_data(request):
    if request.method == 'GET':
        name = request.GET.get('ingredient', None)
        portions = PortionData.objects.filter(food_name=name)
        if portions.exists():
            return Response({"ingredient": name, "portions": list(map(lambda x: {"portion": x.portion, "weight": x.weight}, portions))}, status=status.HTTP_200_OK)
        else:
            return Response({"ingredient": name, "message": "No portion data found"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def density(request):
    if request.method == 'GET':
        name = request.GET.get('ingredient', None)
        try:
            ingredient_name = MasterData.objects.filter(food_name=name)[0]
            print(ingredient_name.density)
            return Response({"Ingredient": name, "Density": ingredient_name.density}, status=status.HTTP_200_OK)
        except Exception as e:
            try:
                ingredient_name = AlternateName.objects.get(
                    alternate_name=name)
                return Response({"ingredient": ingredient_name.food_id.food_name, "density": ingredient_name.food_id.density}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as ex:
                return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def ghg_mass(request):
    if request.method == 'GET':
        name = request.GET.get('ingredient', None)
        portion = request.GET.get('portion', None)
        amount = request.GET.get('amount', None)
        ingredient_name = AlternateName.objects.get(alternate_name=name)
        if ingredient_name is not None:
            master_object = ingredient_name.food_id
            portion_data = PortionData.objects.filter(
                food_id=master_object.id).get(food_unit=portion)
            emission = portion_data.mass * int(amount) * master_object.ghg
            return Response({"Ingredient": master_object.food_name, "Mass": emission}, status=status.HTTP_200_OK)
