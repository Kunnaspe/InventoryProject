from django.db import models

# Department model so that we can keep track of different sections
class Department(models.Model):
    # DepartmentNumber is the primary key
    DepartmentNumber = models.IntegerField(primary_key=True)
    # Stores This department name
    DepartmentName = models.CharField(max_length=100)

    def __str__(self):
        return self.DepartmentName

# Product model for item information
class Product(models.Model):
    # Auto-increment and record product id
    ProductID = models.AutoField(primary_key=True)
    # Stores product name
    ProductName = models.CharField(max_length=200)
    # Must be a unique product number
    ProductNumber = models.CharField(max_length=100, unique=True)
    # Product addition/manufactured date
    ProductDate = models.DateField()
    # Products are linked to the departments
    DepartmentNumber = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.ProductName
