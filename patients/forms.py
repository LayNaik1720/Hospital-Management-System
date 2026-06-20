from django import forms
from django.utils import timezone
from .models import Patient, PatientInsurance

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'blood_group',
            'phone', 'email', 'address', 'emergency_contact_name', 
            'emergency_contact_phone', 'emergency_contact_relation',
            'allergies', 'medical_history'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relation': forms.TextInput(attrs={'class': 'form-control'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth > timezone.now().date():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return date_of_birth

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone

class PatientInsuranceForm(forms.ModelForm):
    class Meta:
        model = PatientInsurance
        fields = [
            'provider_name', 'policy_number', 'group_number',
            'coverage_start_date', 'coverage_end_date', 'is_primary'
        ]
        widgets = {
            'provider_name': forms.TextInput(attrs={'class': 'form-control'}),
            'policy_number': forms.TextInput(attrs={'class': 'form-control'}),
            'group_number': forms.TextInput(attrs={'class': 'form-control'}),
            'coverage_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'coverage_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('coverage_start_date')
        end_date = cleaned_data.get('coverage_end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("Coverage end date must be after start date.")

        return cleaned_data