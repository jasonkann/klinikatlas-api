import time, json, csv, os, datetime
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

def logOutput (filename,status): 
    ct = datetime.datetime.now()
    # Creation 
    if(status=='C'): 
        print(ct + " Erstelle " + filename)
    # Finished 
    if(status=="F"):
        print(ct + " Erstellt: " + filename)

def convertJsonToCsv (filename_base):
    header = ''
    tgtfilename = filename_base + '.csv'
    srcfilename = filename_base + '.json'    
    with open(srcfilename,'r') as json_file:
        jsoncontent = json.load(json_file)
    logOutput(tgtfilename,'C')
    targetfile = open(tgtfilename,'w',newline='')
    # csv.QUOTE_ALL
    csvwriter = csv.writer(targetfile,quoting=csv.QUOTE_NONNUMERIC)
    count = 0 
    for data in jsoncontent:
        if count == 0:
            header == data.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(data.values())
    targetfile.close()
    logOutput(tgtfilename,'F')


def transformToJson(filename_base):
    # tgtfile 
    tgtfilename = filename_base + '.json'
    # srcfile 
    srcfilename = filename_base + '.tmp'
    if not os.path.isfile(tgtfilename): 
        # existiert nicht ....
        logOutput(tgtfilename,'C')
        with open(srcfilename,'r') as fileread1:
            my_dict = fileread1.read().strip()
            l = eval(my_dict)
            #print(json.dumps(l))
        with open(tgtfilename,'w') as filewrite1:
            filewrite1.write(json.dumps(l))
        logOutput(tgtfilename,'F')
    else: 
        print("Datei "+ tgtfilename + " existiert schon, ueberspringe Bearbeitung")

def dump_file(filename_base, filecontent):
    filename = filename_base+".tmp"
    if not os.path.isfile(filename): 
        logOutput(filename,'C')
        with open(filename,'w') as file1:
            pprint(filecontent,file1)
        logOutput(filename,'F')
    else:
        print("Datei "+ filename + " existiert schon, ueberspringe Bearbeitung")
    transformToJson(filename_base)
    convertJsonToCsv(filename_base)


# Enter a context with an instance of the API client
with klinikatlas.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    try:
        # Liste deutscher Orte abrufen
        api_response = api_instance.fileadmin_json_german_places_json_get()
        dump_file('german_places',api_response)
        # list of german states 
        api_response = api_instance.fileadmin_json_german_states_json_get()
        dump_file('german_states', api_response)
        # list of icd_codes 
        api_response = api_instance.fileadmin_json_icd_codes_json_get()
        dump_file('icd_codes', api_response)
        # list of locations_json
        api_response = api_instance.fileadmin_json_locations_json_get()
        dump_file('locations', api_response)
        # list of ops_codes
        api_response = api_instance.fileadmin_json_ops_codes_json_get()
        dump_file('ops_codes',api_response)
        # list of states_json
        api_response = api_instance.fileadmin_json_states_json_get()
        dump_file('states', api_response)
        # pprint(api_response)
    except klinikatlas.ApiException as e:
        print("Exception when calling DefaultApi->fileadmin_json_german_places_json_get: %s\n" % e)