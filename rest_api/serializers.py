from rest_framework import serializers
from rest_api.models import Employee

def multiples_of_1000(value):
    	if value % 1000 !=0:
    		raise serializers.ValidationError("Salary should be multiple of 1000")
def validate(self, data):
    	ename = data.get('ename')
    	esal = data.get('esal')
    	if ename.lower() == 'Manu Mohan':
    		if esal < 60000:
    			raise serializers.ValidationError("Shankar salary minimum 60k")
    	return data 

class EmployeeSerializer(serializers.Serializer):
    eno = serializers.IntegerField()
    ename = serializers.CharField(max_length=64)
    esal = serializers.FloatField(validators = [multiples_of_1000,])
    eaddr = serializers.CharField(max_length=64)
    def  create(self, validated_data):
    	return Employee.objects.create(**validated_data)
    def validate_esal(self, value):
    	""" Validation for the salary """
    	if value < 5000:
    		raise serializers.ValidationError("Employee salary should be minimum 5000")
    	return value

    def update(self, instance, validated_data):
    	instance.eno = validated_data.get('eno', instance.eno)
    	instance.ename = validated_data.get('ename', instance.ename)
    	instance.esal = validated_data.get('esal', instance.esal)
    	instance.eaddr = validated_data.get('eaddr', instance.eaddr)
    	instance.save()
    	return instance

