# Setup

Run the `firsttimesetup` script. Note that you may need to change `pip` in the script to whatever command is in your shell for pip.

To set up the server, run the `runserver` script, the shell script on Unix-based systems and the batch file on Windows.

Afterwards, the API will be hosted on `https://127.0.0.1:8000`.

To access the admin panel, go to `https://127.0.0.1:8000/admin`.

To upload csv data, go to `https://127.0.0.1:8000/upload/`, export the relevant sheet as a tsv file and upload.

# Endpoints

## Ingredients With Foodons `/foodon_ids`
Retrieves all ingredients with Foodon IDs and Alternate Names.

### Response schema 
```
[
	ingredient: string,
	foodon_ids: array,
    alternate_names: array
]
```

## Ingredient From Foodon ID `/foodon/<id>`
Retrieves ingredient data from its Foodon ID. Pass in Foodon ID in URL.

### Response schema
```
{
    food_name: string,
    foodon_id: string
}
```

## Ingredient Data `/ingredient`
Retrieves ingredient data from name.

### Parameters
`ingredient: <ingredient name>`

### Response schema
```
{
	ingredient: string,
    ghg: float
}
```

## Portion Data `/portions`
Retrieves portion data of an ingredient from name.

### Parameters
`ingredient: <ingredient name>`

### Response schema
```
{
	ingredient: string,
    portions: [
    	{
        	portion: string,
        	weight: float
        }
    ]
}
```

## Density `/density`
Retrieves density information from ingredient name.

### Parameters
`ingredient: <ingredient name>`

### Response schema
```
{
	ingredient: string,
    density: float
}
```