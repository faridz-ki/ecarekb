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


def upload_foodon(request):
    if "GET" == request.method:
        return render(request, "csv_form.html")
    # if not GET, then proceed
    try:
        FoodonId.objects.all().delete()
        AlternateName.objects.all().delete()
        csv_file = request.FILES["csv_file"]
        # if not csv_file.name.endswith('.csv'):
        #     messages.error(request, 'File is not CSV type')
        #     return HttpResponseRedirect(reverse("upload"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display
        x = 0
        for line in lines:
            if x == 0:
                x += 1
                continue
            fields = line.split("\t")
            if fields[0] == '':
                break
            try:
                name = fields[0]
                foodon_id = fields[1].split('/')[-1]

                food_id = MasterData.objects.get(food_name=name)

                index = 2
                while fields[index] != '':
                    alt_name = fields[index]
                    try:
                        obj = AlternateName.objects.get(
                            alternate_name=alt_name)
                    except ObjectDoesNotExist as e:
                        obj = AlternateName(
                            food_name=name, food_id=food_id, alternate_name=alt_name)
                        obj.save()
                    index += 1

                entry = FoodonId(
                    food_name=name, food_id=food_id, foodon_id=foodon_id)
                entry.save()
            except Exception as e:
                print(x, repr(e))
                pass
            x += 1

    except Exception as e:
        print(repr(e))

    return HttpResponseRedirect(reverse("upload_foodon"))


def upload(request):

    def isfloat(number):
        try:
            float(number)
            return True
        except ValueError:
            return False
    
    # TODO: add some sort of csv schema check
    if "GET" == request.method:
        return render(request, "csv_form.html")
    # if not GET, then proceed
    try:
        ReferenceData.objects.all().delete()
        MasterData.objects.all().delete()
        csv_file = request.FILES["csv_file"]
        # if not csv_file.name.endswith('.csv'):
        #     messages.error(request, 'File is not CSV type')
        #     return HttpResponseRedirect(reverse("upload"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")

        # retrieve indices from header row
        fields = lines[0].split('\t')
        try:
            name_index = fields.index("Food")
            best_match_index = fields.index("Best match - Global")
            ghg_global_index = fields.index("GHG - Global")
            ghg_retail_index = fields.index("GHG (Mean) - retail")
            category_index = fields.index("Category ")
            density_index = fields.index(
                "Density in g/ml (including mass and bulk density)")
            land_use_index = fields.index("Land Use (Mean)")
            water_use_index = fields.index("Water (95th)")
            land_use_change_index = fields.index("LUC")
            feed_index = fields.index("Feed")
            farm_index = fields.index("Farm")
            processing_index = fields.index("Processing")
            transport_index = fields.index("Transport")
            packaging_index = fields.index("Packging")
            retail_index = fields.index("Retail")
        except Exception as e:
            print(repr(e))

        x = 0
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines[1:]:
            x += 1
            fields = line.split("\t")
            fields = list(map(lambda x: x.strip(), fields))
            if fields[0] == '':
                break
            try:
                ghg_retail = fields[ghg_retail_index]
                if not isfloat(ghg_retail):
                    ghg_retail = 0
                ghg_global = fields[ghg_global_index]
                if not isfloat(ghg_global):
                    ghg_global = 0
                name = fields[name_index]
                category = fields[category_index]
                best_match = fields[best_match_index]
                density = fields[density_index]
                if density == '':
                    density = 1

                # Prevent dupes
                if MasterData.objects.filter(food_name=name).exists():
                    continue

                try:
                    best_match_id = ReferenceData.objects.get(
                        food_name=best_match)
                except ObjectDoesNotExist as e:
                    # create new ReferenceData record
                    land_use = fields[land_use_index]
                    water_use = fields[water_use_index]
                    land_use_change = fields[land_use_change_index]
                    print(land_use_change, isfloat(land_use_change))
                    if not isfloat(land_use_change):
                        land_use_change = 0
                    feed = fields[feed_index]
                    if not isfloat(feed):
                        feed = 0
                    farm = fields[farm_index]
                    if not isfloat(farm):
                        farm = 0
                    processing = fields[processing_index]
                    if not isfloat(processing):
                        processing = 0
                    transport = fields[transport_index]
                    if not isfloat(transport):
                        transport = 0
                    packaging = fields[packaging_index]
                    if not isfloat(packaging):
                        packaging = 0
                    retail = fields[retail_index]
                    if not isfloat(retail):
                        retail = 0
                    ref = ReferenceData(ghg_global=ghg_global,                               ghg_retail=ghg_retail,food_name=best_match,land_use=land_use, water_use=water_use,land_use_change=land_use_change, feed=feed,farm=farm, processing=processing, transport=transport, packaging=packaging, retail=retail)
                    ref.save()
                    best_match_id = ref

                entry = MasterData(ghg_global=ghg_global, ghg_retail=ghg_retail, food_name=name, category=category,
                                   best_match=best_match, best_match_id=best_match_id, density=density)
                entry.save()
            except Exception as e:
                print(x, repr(e))
                pass

    except Exception as e:
        print(repr(e))

    return HttpResponseRedirect(reverse("upload"))

def upload_portion(request):
    if "GET" == request.method:
        return render(request, "csv_form.html")
    # if not GET, then proceed
    try:
        PortionData.objects.all().delete()
        csv_file = request.FILES["csv_file"]
        # if not csv_file.name.endswith('.csv'):
        #     messages.error(request, 'File is not CSV type')
        #     return HttpResponseRedirect(reverse("upload"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        fields = lines[0].split('\t')
        print(fields)
        try:
            name_index = fields.index("Food")
            description_index = fields.index("description")
            portion_index = fields.index("portion")
            weight_index = fields.index("weight")
            available_index = fields.index("available\r")
        except Exception as e:
            print(repr(e))

        # loop over the lines and save them in db. If error , store as string and then display
        x = 1
        for line in lines[1:]:
            fields = line.split("\t")
            if fields[0] == '':
                break
            try:
                available = fields[available_index]
                name = fields[name_index]
                description = fields[description_index]
                food_id = MasterData.objects.get(food_name=name)
                portion = fields[portion_index]
                weight = fields[weight_index]
                if weight == '':
                    continue
                # Check for duplicate
                dupe = PortionData.objects.filter(food_name=name).filter(portion=portion)
                if dupe.exists():
                    continue
                entry = PortionData(
                    food_name=name, food_id=food_id, portion=portion, weight=weight, description=description)
                entry.save()
            except Exception as e:
                print(x, repr(e))
                pass
            x += 1
    except Exception as e:
        print(repr(e))

    return HttpResponseRedirect(reverse("upload_foodon"))

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
