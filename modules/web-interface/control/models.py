from django.db import models

# Create your models here.

class TiberiusRobot(models.Model):
	#Basic details
	name = models.CharField(max_length = 50)
	ip_address = models.GenericIPAddressField(protocol = 'IPv4')
	mac_address = models.CharField(max_length = 30)

	#Enabled Modules
	control_enabled = models.BooleanField()
	autonomy_enabled = models.BooleanField()
	object_detection_enabled = models.BooleanField()
	database_enabled = models.BooleanField()

	image = models.ImageField()
