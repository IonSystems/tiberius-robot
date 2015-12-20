from django.db import models

from django.contrib.auth.models import User

class Robot(models.Model):
	#Basic details
	name = models.CharField(max_length = 50)
	ip_address = models.GenericIPAddressField(protocol = 'IPv4')
	mac_address = models.CharField(max_length = 30)

	#Weight in Kg
	weight = models.DecimalField(max_digits=3, decimal_places=2)

	#Battery capacity in mAH
	capacity = models.DecimalField(max_digits=5, decimal_places=2)

	#Owner of the robot
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default = '0', related_name = "robot_owner")

	#Permitted users of the robot
	permitted_users = models.ManyToManyField(User, related_name = "robot_permitted_users")

	#Enabled Modules
	control_enabled = models.BooleanField()
	autonomy_enabled = models.BooleanField()
	object_detection_enabled = models.BooleanField()
	database_enabled = models.BooleanField()

	#An image of the robot
	image = models.ImageField()
