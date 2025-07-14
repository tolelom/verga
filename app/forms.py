from django import forms
from .models import BirthChart

class BirthChartForm(forms.ModelForm):
    class Meta:
        model = BirthChart
        fields = ['name', 'birth_date', 'birth_time', 'birth_location']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': '홍길동'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-purple-500'
            }),
            'birth_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-purple-500'
            }),
            'birth_location': forms.TextInput(attrs={
                'class': 'w-full p-3 pl-10 rounded-lg bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': '서울 특별시, 대한민국'
            })
        }
        labels = {
            'name': '이름',
            'birth_date': '생년월일',
            'birth_time': '출생 시간',
            'birth_location': '출생지'
        }