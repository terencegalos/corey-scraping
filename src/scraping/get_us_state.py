def get_state(zip_string):
    # Ensure param is a string to prevent unpredictable parsing results
    if not isinstance(zip_string, str):
        print('Must pass the zipcode as a string.')
        return

    # Ensure we have exactly 5 characters to parse
    if len(zip_string) != 5:
        print('Must pass a 5-digit zipcode.')
        return

    # Ensure we don't parse strings starting with 0 as octal values
    zip_code = int(zip_string)

    # Code cases alphabetized by state
    if 35000 <= zip_code <= 36999:
        st = 'AL'
        state = 'Alabama'
    elif 99500 <= zip_code <= 99999:
        st = 'AK'
        state = 'Alaska'
    elif 85000 <= zip_code <= 86999:
        st = 'AZ'
        state = 'Arizona'
    elif 71600 <= zip_code <= 72999:
        st = 'AR'
        state = 'Arkansas'
    elif 90000 <= zip_code <= 96699:
        st = 'CA'
        state = 'California'
    elif 80000 <= zip_code <= 81999:
        st = 'CO'
        state = 'Colorado'
    elif (6000 <= zip_code <= 6389) or (6391 <= zip_code <= 6999):
        st = 'CT'
        state = 'Connecticut'
    elif 19700 <= zip_code <= 19999:
        st = 'DE'
        state = 'Delaware'
    elif 32000 <= zip_code <= 34999:
        st = 'FL'
        state = 'Florida'
    elif (30000 <= zip_code <= 31999) or (39800 <= zip_code <= 39999):
        st = 'GA'
        state = 'Georgia'
    elif 96700 <= zip_code <= 96999:
        st = 'HI'
        state = 'Hawaii'
    elif 83200 <= zip_code <= 83999 and zip_code != 83414:
        st = 'ID'
        state = 'Idaho'
    elif 60000 <= zip_code <= 62999:
        st = 'IL'
        state = 'Illinois'
    elif 46000 <= zip_code <= 47999:
        st = 'IN'
        state = 'Indiana'
    elif 50000 <= zip_code <= 52999:
        st = 'IA'
        state = 'Iowa'
    elif 66000 <= zip_code <= 67999:
        st = 'KS'
        state = 'Kansas'
    elif 40000 <= zip_code <= 42999:
        st = 'KY'
        state = 'Kentucky'
    elif 70000 <= zip_code <= 71599:
        st = 'LA'
        state = 'Louisiana'
    elif 3900 <= zip_code <= 4999:
        st = 'ME'
        state = 'Maine'
    elif 20600 <= zip_code <= 21999:
        st = 'MD'
        state = 'Maryland'
    elif (1000 <= zip_code <= 2799) or (zip_code == 5501) or (zip_code == 5544):
        st = 'MA'
        state = 'Massachusetts'
    elif 48000 <= zip_code <= 49999:
        st = 'MI'
        state = 'Michigan'
    elif 55000 <= zip_code <= 56899:
        st = 'MN'
        state = 'Minnesota'
    elif 38600 <= zip_code <= 39999:
        st = 'MS'
        state = 'Mississippi'
    elif 63000 <= zip_code <= 65999:
        st = 'MO'
        state = 'Missouri'
    elif 59000 <= zip_code <= 59999:
        st = 'MT'
        state = 'Montana'
    elif 27000 <= zip_code <= 28999:
        st = 'NC'
        state = 'North Carolina'
    elif 58000 <= zip_code <= 58999:
        st = 'ND'
        state = 'North Dakota'
    elif 68000 <= zip_code <= 69999:
        st = 'NE'
        state = 'Nebraska'
    elif 88900 <= zip_code <= 89999:
        st = 'NV'
        state = 'Nevada'
    elif 3000 <= zip_code <= 3899:
        st = 'NH'
        state = 'New Hampshire'
    elif 7000 <= zip_code <= 8999:
        st = 'NJ'
        state = 'New Jersey'
    elif 87000 <= zip_code <= 88499:
        st = 'NM'
        state = 'New Mexico'
    elif (10000 <= zip_code <= 14999) or (zip_code == 6390) or (zip_code == 501) or (zip_code == 544):
        st = 'NY'
        state = 'New York'
    elif 43000 <= zip_code <= 45999:
        st = 'OH'
        state = 'Ohio'
    elif (73000 <= zip_code <= 73199) or (73400 <= zip_code <= 74999):
        st = 'OK'
        state = 'Oklahoma'
    elif 97000 <= zip_code <= 97999:
        st = 'OR'
        state = 'Oregon'
    elif 15000 <= zip_code <= 19699:
        st = 'PA'
        state = 'Pennsylvania'
    elif 300 <= zip_code <= 999:
        st = 'PR'
        state = 'Puerto Rico'
    elif 2800 <= zip_code <= 2999:
        st = 'RI'
        state = 'Rhode Island'
    elif 29000 <= zip_code <= 29999:
        st = 'SC'
        state = 'South Carolina'
    elif 57000 <= zip_code <= 57999:
        st = 'SD'
        state = 'South Dakota'
    elif 37000 <= zip_code <= 38599:
        st = 'TN'
        state = 'Tennessee'
    elif (75000 <= zip_code <= 79999) or (73301 <= zip_code <= 73399) or (88500 <= zip_code <= 88599):
        st = 'TX'
        state = 'Texas'
    elif 84000 <= zip_code <= 84999:
        st = 'UT'
        state = 'Utah'
    elif 5000 <= zip_code <= 5999:
        st = 'VT'
        state = 'Vermont'
    elif (20100 <= zip_code <= 20199) or (22000 <= zip_code <= 24699) or (zip_code == 20598):
        st = 'VA'
        state = 'Virginia'
    elif (20000 <= zip_code <= 20099) or (20200 <= zip_code <= 20599) or (56900 <= zip_code <= 56999):
        st = 'DC'
        state = 'Washington DC'
    elif 98000 <= zip_code <= 99499:
        st = 'WA'
        state = 'Washington'
    elif 24700 <= zip_code <= 26999:
        st = 'WV'
        state = 'West Virginia'
    elif 53000 <= zip_code <= 54999:
        st = 'WI'
        state = 'Wisconsin'
    elif (82000 <= zip_code <= 83199) or zip_code == 83414:
        st = 'WY'
        state = 'Wyoming'
    else:
        st = 'none'
        state = 'none'
        print('No state found matching', zip_code)

    # Return `state` for the full name or `st` for the postal abbreviation
    return state

# Example usage:
# zipcode_input = "33716"
# result = get_state('33716')#zipcode_input)
# print(result)
