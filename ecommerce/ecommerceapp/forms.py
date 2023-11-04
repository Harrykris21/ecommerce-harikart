from django import forms
from ecommerceapp.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField (widget=forms.Textarea(attrs={'placeholder': "Write review"}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']