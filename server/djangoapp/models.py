# Uncomment the following imports before adding the Model code

from django.db import models

# from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100)  # Car make name
    description = models.TextField()  # Car make description

    # Other fields as needed

    def __str__(self):
        return self.name  # String representation of the car make


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

# CarModel model


class CarModel(models.Model):
    # ForeignKey to CarMake model, establishing many-to-one relationship
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    # Dealer ID from the external Cloudant database
    dealer_id = models.IntegerField()

    # Name of the car model
    name = models.CharField(max_length=100)

    # Car type with limited choices
    CAR_TYPES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        ("TRUCK", "Truck"),
        ("COUPE", "Coupe"),
        ("CONVERTIBLE", "Convertible"),
    ]
    type = models.CharField(max_length=11, choices=CAR_TYPES, default="SUV")

    # Year with validators for minimum and maximum
    year = models.IntegerField(
        validators=[
            MaxValueValidator(2024),  # Update this if needed
            MinValueValidator(1990),
        ]
    )

    # Other fields as needed

    def __str__(self):
        # Return car make and model name as string representation
        return f"{self.car_make.name} {self.name}"
