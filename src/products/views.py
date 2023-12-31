from django.shortcuts import render
from .models import Product, Purchase
import pandas as pd
from .utils import get_simple_plot

# Create your views here.

def chart_select_view(request):
    graph = None
    error_message=None
    df = None


    product_df = pd.DataFrame(Product.objects.all().values())
    purchase_df = pd.DataFrame(Purchase.objects.all().values())
    product_df['product_id'] = product_df['id']

    if purchase_df.shape[0] > 0:
        df = pd.merge(purchase_df, product_df, on='product_id').drop(['id_y', 'date_y'], axis=1).rename({'id_x':'id', 'date_x':'date'}, axis=1)
        if request.method == 'POST':
            chart_type = request.POST.get('sales')
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']
            #print(df)
            df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')

            if chart_type != "":
                if date_from != "" and date_to != "":
                    df = df[(df['date']>date_from) & (df['date']<date_to)]
                    df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')
                # function to get a graph
                graph = get_simple_plot(chart_type, x=df2['date'], y=df2['total_price'], data=df)
            else:
                error_message = 'Please choose a chart type to continue'


        else:
            error_message = 'No records in the database'
            



    context = {
        'graph' : graph,
        'error_message': error_message,
        

    }
    return render(request, 'products/main.html', context)

