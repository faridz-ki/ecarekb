from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from app.models import MasterData, PortionData, AlternateName, FoodonId, ReferenceData, SeasonalityData

def upload_foodon(request):
    if "GET" == request.method:
        return render(request, "admin/csv_form.html")
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
                for x in range(2, len(fields)):
                    if fields[x] == '':
                        break
                    alt_name = fields[x]
                    try:
                        obj = AlternateName.objects.get(
                            alternate_name=alt_name)
                    except ObjectDoesNotExist as e:
                        obj = AlternateName(
                            food_name=name, food_id=food_id, alternate_name=alt_name)
                        obj.save()

                entry = FoodonId(
                    food_name=name, food_id=food_id, foodon_id=foodon_id)
                entry.save()
            except Exception as e:
                print(x, repr(e))
                pass
            x += 1

    except Exception as e:
        print(repr(e))

    return HttpResponseRedirect(reverse("admin:upload_foodon"))


def upload(request):

    def isfloat(number):
        try:
            float(number)
            return True
        except ValueError:
            return False
    
    # TODO: add some sort of csv schema check
    if "GET" == request.method:
        return render(request, "admin/csv_form.html")
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
            water_use_index = fields.index(" Water (95th)")
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

    return HttpResponseRedirect(reverse("admin:upload"))

def upload_portion(request):
    if "GET" == request.method:
        return render(request, "admin/csv_form.html")
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

    return HttpResponseRedirect(reverse("admin:upload_foodon"))

def upload_seasonality(request):
    if "GET" == request.method:
        return render(request, "admin/csv_form.html")
    # if not GET, then proceed
    try:
        SeasonalityData.objects.all().delete()

        csv_file = request.FILES["csv_file"]
        # if not csv_file.name.endswith('.csv'):
        #     messages.error(request, 'File is not CSV type')
        #     return HttpResponseRedirect(reverse("upload"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display
        for x in range(2, len(lines)):
            fields = lines[x].split("\t")
            if fields[0] == '':
                break
            try:
                name = fields[0]
                obj = ReferenceData.objects.get(food_name=name)
                month = 1
                while month <= 12:
                    offset = (month - 1) * 7
                    luc = float(fields[offset + 1])
                    feed = float(fields[offset + 2])
                    farm = float(fields[offset + 3])
                    processing = float(fields[offset + 4])
                    transport = float(fields[offset + 5])
                    packaging = float(fields[offset + 6])
                    retail = float(fields[offset + 7])

                    ghg = luc*obj.land_use_change + feed*obj.feed + farm*obj.farm + processing*obj.processing + transport*obj.transport + packaging*obj.packaging + retail*obj.retail

                    entry = SeasonalityData(food_name=name, land_use_change=luc, feed=feed, farm=farm, processing=processing, transport=transport, packaging=packaging, retail=retail, month=month, reference_id=obj, ghg=ghg)
                    entry.save()
                    month += 1
            except Exception as e:
                print(x, repr(e))
                pass

    except Exception as e:
        print(repr(e))

    return HttpResponseRedirect(reverse("admin:upload_seasonality"))
