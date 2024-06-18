import math
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import CalculationAttempt  # Import the model for saving attempts


# Create your views here.
def index(request):
    return render(request, 'index.html')




def calculate(request):
    if request.method == 'POST':
        # Extracting data from the POST request
        Qh = float(request.POST.get('Qh'))
        Qc = float(request.POST.get('Qc'))
        Mh = float(request.POST.get('Mh'))
        Ch = float(request.POST.get('Ch'))
        THin = float(request.POST.get('THin'))
        THout = float(request.POST.get('THout'))
        Mc = float(request.POST.get('Mc'))
        Cc = float(request.POST.get('Cc'))
        TCout = float(request.POST.get('TCout'))
        TCin = float(request.POST.get('TCin'))
        Do = float(request.POST.get('Do'))
        L = float(request.POST.get('L'))
        NUi = float(request.POST.get('NUi'))
        k = float(request.POST.get('k'))
        Pin = float(request.POST.get('Pin'))
        pout = float(request.POST.get('pout'))

        # Calculate Qav
        Qav = (Qh + Qc) / 2

        # Calculate Aav
        Aav = 3.14159 * Do * L  # Using pi value instead of pi constant

        # Calculate lmtD
        if (THin - TCout) != (THout - TCin):
            lmtD = ((THin - TCout) - (THout - TCin)) / math.log(abs((THin - TCout) / (THout - TCin)))
        else:
            # Handle the case where the denominator is zero
            lmtD = float('inf')  # Assigning infinity or any appropriate value as per your requirement

        # Calculate Hi
        Hi = NUi * k / Do

        # Calculate Uav
        Uav = Qav / (Aav * lmtD)

        # Calculating Qh and Qc
        Qh = Mh * Ch * (THin - THout)
        Qc = Mc * Cc * (TCout - TCin)

        # Calculating Aav
        Aav = 3.14159 * Do * L  # Using pi value instead of pi constant

        # Calculating Hi and lmtD
        Hi = NUi * k / Do
        lmtD = ((THin - TCout) - (THout - TCin)) / math.log(abs((THin - TCout) / (THout - TCin)))

        # Calculate h
        if Uav != 0 and Hi != 0:
            h = 1 / ((1/Uav) - (1/Hi))
        else:
            # Handle the case where Uav or Hi is zero
            h = float('inf')  # Assigning infinity or any appropriate value as per your requirement

        # Calculate E
        E = (THin - THout) / (THin - TCin)

        # Calculate P
        P = Pin - pout

        attempt = CalculationAttempt(
            h=h,  # Assuming 'h' and 'p' are calculated earlier in the code
            p=P,  # Replace 'p' with the variable name you're using
        )
        attempt.save()


        # Prepare context to pass to the template
        context = {
            'h': h,
            'E': E,
            'P': P,
            'Qh': Qh,
            'Qc': Qc,
            'Aav': Aav,
            'Hi': Hi,
            'lmtD': lmtD
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


@csrf_exempt  # Add this decorator if CSRF protection is enabled and not using CSRF tokens for AJAX requests
def get_data(request):
    if request.method == 'GET':
        # Assuming you have a model named YourModel with fields 'p' and 'h'
        queryset = CalculationAttempt.objects.all().order_by('p')  # Fetch all objects, ordered by 'p'
        data = CalculationAttempt.objects.all()
    
        # Extract 'p' and 'h' values from the queryset
        p_values = [obj.p for obj in queryset]
        h_values = [obj.h for obj in queryset]

        # Construct a dictionary containing the 'p' and 'h' values
        data = {
            'pValues': p_values,
            'hValues': h_values
        }

        # Return the data as JSON response
        return JsonResponse(data)


def delete_data(request):
    CalculationAttempt.objects.all().delete()
    return redirect(index)