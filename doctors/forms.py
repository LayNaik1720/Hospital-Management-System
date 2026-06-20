from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Doctor, Department, DoctorSchedule, Nurse

User = get_user_model()

class DoctorForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='doctor', doctor__isnull=True),
        empty_label="Select a doctor user account"
    )
    
    class Meta:
        model = Doctor
        fields = ['user', 'license_number', 'specialization', 'department', 
                 'qualification', 'experience_years', 'consultation_fee', 'room_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'user',
            Row(
                Column('license_number', css_class='form-group col-md-6 mb-0'),
                Column('specialization', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('department', css_class='form-group col-md-6 mb-0'),
                Column('experience_years', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'qualification',
            Row(
                Column('consultation_fee', css_class='form-group col-md-6 mb-0'),
                Column('room_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Doctor', css_class='btn btn-primary')
        )

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'head_of_department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            'head_of_department',
            Submit('submit', 'Save Department', css_class='btn btn-primary')
        )

class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['day_of_week', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'day_of_week',
            Row(
                Column('start_time', css_class='form-group col-md-6 mb-0'),
                Column('end_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Add Schedule', css_class='btn btn-primary')
        )

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError('End time must be after start time.')
        
        return cleaned_data

class NurseForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='nurse', nurse__isnull=True),
        empty_label="Select a nurse user account"
    )
    
    class Meta:
        model = Nurse
        fields = ['user', 'license_number', 'department', 'shift', 'experience_years']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'user',
            Row(
                Column('license_number', css_class='form-group col-md-6 mb-0'),
                Column('department', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('shift', css_class='form-group col-md-6 mb-0'),
                Column('experience_years', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Nurse', css_class='btn btn-primary')
        )