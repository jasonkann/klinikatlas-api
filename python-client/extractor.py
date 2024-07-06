import time, json
from deutschland import klinikatlas
from pprint import pprint
from deutschland.klinikatlas.api import default_api
from deutschland.klinikatlas.model.fileadmin_json_german_places_json_get200_response_inner import FileadminJsonGermanPlacesJsonGet200ResponseInner
from deutschland.klinikatlas.model.fileadmin_json_german_states_json_get200_response_inner import FileadminJsonGermanStatesJsonGet200ResponseInner
from deutschland.klinikatlas.model.fileadmin_json_icd_codes_json_get200_response_inner import FileadminJsonIcdCodesJsonGet200ResponseInner
from deutschland.klinikatlas.model.fileadmin_json_locations_json_get200_response_inner import FileadminJsonLocationsJsonGet200ResponseInner
from deutschland.klinikatlas.model.fileadmin_json_ops_codes_json_get200_response_inner import FileadminJsonOpsCodesJsonGet200ResponseInner
from deutschland.klinikatlas.model.fileadmin_json_states_json_get200_response_inner import FileadminJsonStatesJsonGet200ResponseInner
from deutschland.klinikatlas.model.searchresults_get200_response import SearchresultsGet200Response
# Defining the host is optional and defaults to https://klinikatlas.api.proxy.bund.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = klinikatlas.Configuration(
    host = "https://klinikatlas.api.proxy.bund.dev"
)

def dump_file(filename, filecontent):
    with open(filename,'w') as file1:
        for line in filecontent:
            file1.write("%s" % line)

# Enter a context with an instance of the API client
with klinikatlas.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    try:
        # Liste deutscher Orte abrufen
        api_response = api_instance.fileadmin_json_german_places_json_get()
        # dump the json-file
        dump_file('german_places.json',api_response)
        # list of german states 
        api_response = api_instance.fileadmin_json_german_states_json_get()
        dump_file('german_states.json', api_response)
        # list of icd_codes 
        api_response = api_instance.fileadmin_json_icd_codes_json_get()
        dump_file('icd_codes.json', api_response)
        # list of locations_json
        api_response = api_instance.fileadmin_json_locations_json_get()
        dump_file('locations.json', api_response)
        # list of ops_codes
        api_response = api_instance.fileadmin_json_ops_codes_json_get()
        dump_file('ops_codes.json',api_response)
        # list of states_json
        api_response = api_instance.fileadmin_json_states_json_get()
        dump_file('states.json', api_response)

        # pprint(api_response)
    except klinikatlas.ApiException as e:
        print("Exception when calling DefaultApi->fileadmin_json_german_places_json_get: %s\n" % e)