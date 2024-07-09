import time, json, csv, os
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

def convertJsonToCsv (srcfilename):
    header = ''
    length = len(srcfilename)
    targetfilename = srcfilename[:length-3]+'.csv'
    with open(srcfilename) as json_file:
        jsoncontent = json.loads(json_file)  
    targetfile = open(targetfilename,'w',newline='')
    csvwriter = csv.writer(targetfile)
    count = 0 
    for data in jsoncontent:
        if count == 0:
            header == data.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(data.values())
    targetfile.close()


def transformToJson(filename):
    if not os.path.isfile(filename+'.new'): 
        # existiert nicht ....
        print("Bearbeite "+filename+"...")
        with open(filename,'r') as fileread1:
            my_dict = fileread1.read().strip()
            l = eval(my_dict)
            #print(json.dumps(l))
        with open(filename+'.new','w') as filewrite1:
            filewrite1.write(json.dumps(l))
    else: 
        print("Datei "+ filename + " existiert schon, ueberspringe Bearbeitung")

def dump_file(filename, filecontent):
    if not os.path.isfile(filename): 
        with open(filename,'w') as file1:
            pprint(filecontent,file1)
    else:
        print("Datei "+ filename + " existiert schon, ueberspringe Bearbeitung")
    transformToJson(filename)
    # convertJsonToCsv(filename)


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
        api_response

        # pprint(api_response)
    except klinikatlas.ApiException as e:
        print("Exception when calling DefaultApi->fileadmin_json_german_places_json_get: %s\n" % e)