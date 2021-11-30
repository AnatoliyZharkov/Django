from rest_framework import serializers
from datetime import timedelta
from django.contrib.auth import authenticate

from .models import Department, Positions, Worker, PosHistory, VacHistory, User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name_of_dep', 'abbreviation', 'head')


class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = ('id', 'name', 'salary', 'num_of_vac_days')


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id', 'full_name', 'passport_data', 'date_of_birth', 'place_of_birth',
                  'address', 'depart', 'pos', 'experience', 'salary', 'status')


class PosHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PosHistory
        fields = ('id', 'worker', 'worker_pos', 'start_date', 'end_date')


class VacHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VacHistory
        fields = ('id', 'worker', 'start_date', 'that_time_pos', 'num_of_days')


class WorkerForTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('full_name',)


class FirstTaskSerializer(serializers.ModelSerializer):
    workers = WorkerForTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('name_of_dep', 'workers')


class SecondTaskSerializer(serializers.ModelSerializer):
    vac_start = serializers.SerializerMethodField('vac_start_date')
    vac_end = serializers.SerializerMethodField('vac_end_date')
    days_sum = serializers.SerializerMethodField('days')

    class Meta:
        model = Worker
        fields = ('full_name', 'vac_start', 'vac_end', 'days_sum')

    def vac_start_date(self, obj):
        for i in VacHistory.objects.filter(worker__exact=obj.id):
            return i.start_date

    def vac_end_date(self, obj):
        for i in VacHistory.objects.filter(worker__exact=obj.id):
            return i.start_date + timedelta(days=i.num_of_days)

    def days(self, obj):
        sum_of_days = 0
        for i in VacHistory.objects.filter(worker__exact=obj.id):
            sum_of_days += i.num_of_days
        return sum_of_days


class ThirdTaskSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField('worker_pos')

    class Meta:
        model = Worker
        fields = ('full_name', 'position', 'salary')

    def worker_pos(self, obj):
        for i in Positions.objects.filter(name__exact=obj.pos):
            return i.name


class FourthTaskSerializer(serializers.ModelSerializer):
    workers = serializers.SerializerMethodField('workers_count')

    class Meta:
        model = Department
        fields = ('name_of_dep', 'head', 'workers')

    def workers_count(self, obj):
        return Worker.objects.filter(depart__exact=obj.id).count()
