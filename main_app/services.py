import requests

def get_medications(generic_name):
    url = 'https://api.fda.gov/drug/ndc.json'
    params = {'generic_name': generic_name}
    r = requests.get(url, params=params)
    medications = r.json()
    medications_list = {'medications': medications[results]}
    return medications_list

    # brand_name = models.CharField(max_length=100)
    # generic_name = models.CharField(max_length=100)
    # product_ndc = models.CharField(max_length=100)
    # dosage_form = models.CharField(max_length=100)
    # strength = models.CharField(max_length=100)
    # active_ingredient = models.CharField(max_length=100)
    # description = models.CharField(max_length=200)