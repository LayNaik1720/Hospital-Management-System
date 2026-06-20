from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'patient', 'doctor', 'appointment_date', 'appointment_time',
            'duration_minutes', 'appointment_type', 'reason', 'notes'
        ]
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'min': ''}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set minimum date to today
        from datetime import date
        self.fields['appointment_date'].widget.attrs['min'] = date.today().strftime('%Y-%m-%d')
        
        # Filter active patients and doctors
        self.fields['patient'].queryset = Patient.objects.filter(is_active=True)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_available=True)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='form-group col-md-6 mb-0'),
                Column('doctor', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('appointment_date', css_class='form-group col-md-4 mb-0'),
                Column('appointment_time', css_class='form-group col-md-4 mb-0'),
                Column('duration_minutes', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'appointment_type',
            'reason',
            'notes',
            Submit('submit', 'Schedule Appointment', css_class='btn btn-primary')
        )

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        doctor = cleaned_data.get('doctor')
        
        if appointment_date and appointment_time and doctor:
            from datetime import date, datetime, timedelta
            
            # Check if appointment is in the past
            if appointment_date < date.today():
                raise forms.ValidationError('Cannot schedule appointments in the past.')
            
            if appointment_date == date.today():
                current_time = datetime.now().time()
                if appointment_time <= current_time:
                    raise forms.ValidationError('Cannot schedule appointments in the past.')
            
            # Check doctor availability for the day
            day_of_week = appointment_date.weekday()
            doctor_schedules = doctor.schedules.filter(day_of_week=day_of_week, is_active=True)
            
            if not doctor_schedules.exists():
                raise forms.ValidationError(f'Doctor is not available on {appointment_date.strftime("%A")}.')
            
            # Check if time falls within doctor's schedule
            time_available = False
            for schedule in doctor_schedules:
                if schedule.start_time <= appointment_time <= schedule.end_time:
                    time_available = True
                    break
            
            if not time_available:
                raise forms.ValidationError('Selected time is outside doctor\'s working hours.')
        
        return cleaned_data

class RescheduleForm(forms.Form):
    new_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='New Date'
    )
    new_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='New Time'
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Reason for Rescheduling'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set minimum date to today
        from datetime import date
        self.fields['new_date'].widget.attrs['min'] = date.today().strftime('%Y-%m-%d')
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('new_date', css_class='form-group col-md-6 mb-0'),
                Column('new_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'reason',
            Submit('submit', 'Reschedule Appointment', css_class='btn btn-warning')
        )

    def clean(self):
        cleaned_data = super().clean()
        new_date = cleaned_data.get('new_date')
        new_time = cleaned_data.get('new_time')
        
        if new_date and new_time:
            from datetime import date, datetime
            
            # Check if new appointment is in the past
            if new_date < date.today():
                raise forms.ValidationError('Cannot reschedule to a past date.')
            
            if new_date == date.today():
                current_time = datetime.now().time()
                if new_time <= current_time:
                    raise forms.ValidationError('Cannot reschedule to a past time.')
        
        return cleaned_data