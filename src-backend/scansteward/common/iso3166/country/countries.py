from typing import Final

from scansteward.common.iso3166.models import Country

ALPHA2_CODE_TO_COUNTRIES: Final[dict[str, Country]] = {
    "AW": Country("AW", "Aruba"),
    "AF": Country("AF", "Afghanistan"),
    "AO": Country("AO", "Angola"),
    "AI": Country("AI", "Anguilla"),
    "AX": Country("AX", "Åland Islands"),
    "AL": Country("AL", "Albania"),
    "AD": Country("AD", "Andorra"),
    "AE": Country("AE", "United Arab Emirates"),
    "AR": Country("AR", "Argentina"),
    "AM": Country("AM", "Armenia"),
    "AS": Country("AS", "American Samoa"),
    "AQ": Country("AQ", "Antarctica"),
    "TF": Country("TF", "French Southern Territories"),
    "AG": Country("AG", "Antigua and Barbuda"),
    "AU": Country("AU", "Australia"),
    "AT": Country("AT", "Austria"),
    "AZ": Country("AZ", "Azerbaijan"),
    "BI": Country("BI", "Burundi"),
    "BE": Country("BE", "Belgium"),
    "BJ": Country("BJ", "Benin"),
    "BQ": Country("BQ", "Bonaire, Sint Eustatius and Saba"),
    "BF": Country("BF", "Burkina Faso"),
    "BD": Country("BD", "Bangladesh"),
    "BG": Country("BG", "Bulgaria"),
    "BH": Country("BH", "Bahrain"),
    "BS": Country("BS", "Bahamas"),
    "BA": Country("BA", "Bosnia and Herzegovina"),
    "BL": Country("BL", "Saint Barthélemy"),
    "BY": Country("BY", "Belarus"),
    "BZ": Country("BZ", "Belize"),
    "BM": Country("BM", "Bermuda"),
    "BO": Country("BO", "Bolivia"),
    "BR": Country("BR", "Brazil"),
    "BB": Country("BB", "Barbados"),
    "BN": Country("BN", "Brunei Darussalam"),
    "BT": Country("BT", "Bhutan"),
    "BV": Country("BV", "Bouvet Island"),
    "BW": Country("BW", "Botswana"),
    "CF": Country("CF", "Central African Republic"),
    "CA": Country("CA", "Canada"),
    "CC": Country("CC", "Cocos (Keeling) Islands"),
    "CH": Country("CH", "Switzerland"),
    "CL": Country("CL", "Chile"),
    "CN": Country("CN", "China"),
    "CI": Country("CI", "Côte d'Ivoire"),
    "CM": Country("CM", "Cameroon"),
    "CD": Country("CD", "Congo, The Democratic Republic of the"),
    "CG": Country("CG", "Congo"),
    "CK": Country("CK", "Cook Islands"),
    "CO": Country("CO", "Colombia"),
    "KM": Country("KM", "Comoros"),
    "CV": Country("CV", "Cabo Verde"),
    "CR": Country("CR", "Costa Rica"),
    "CU": Country("CU", "Cuba"),
    "CW": Country("CW", "Curaçao"),
    "CX": Country("CX", "Christmas Island"),
    "KY": Country("KY", "Cayman Islands"),
    "CY": Country("CY", "Cyprus"),
    "CZ": Country("CZ", "Czechia"),
    "DE": Country("DE", "Germany"),
    "DJ": Country("DJ", "Djibouti"),
    "DM": Country("DM", "Dominica"),
    "DK": Country("DK", "Denmark"),
    "DO": Country("DO", "Dominican Republic"),
    "DZ": Country("DZ", "Algeria"),
    "EC": Country("EC", "Ecuador"),
    "EG": Country("EG", "Egypt"),
    "ER": Country("ER", "Eritrea"),
    "EH": Country("EH", "Western Sahara"),
    "ES": Country("ES", "Spain"),
    "EE": Country("EE", "Estonia"),
    "ET": Country("ET", "Ethiopia"),
    "FI": Country("FI", "Finland"),
    "FJ": Country("FJ", "Fiji"),
    "FK": Country("FK", "Falkland Islands (Malvinas)"),
    "FR": Country("FR", "France"),
    "FO": Country("FO", "Faroe Islands"),
    "FM": Country("FM", "Micronesia, Federated States of"),
    "GA": Country("GA", "Gabon"),
    "GB": Country("GB", "United Kingdom"),
    "GE": Country("GE", "Georgia"),
    "GG": Country("GG", "Guernsey"),
    "GH": Country("GH", "Ghana"),
    "GI": Country("GI", "Gibraltar"),
    "GN": Country("GN", "Guinea"),
    "GP": Country("GP", "Guadeloupe"),
    "GM": Country("GM", "Gambia"),
    "GW": Country("GW", "Guinea-Bissau"),
    "GQ": Country("GQ", "Equatorial Guinea"),
    "GR": Country("GR", "Greece"),
    "GD": Country("GD", "Grenada"),
    "GL": Country("GL", "Greenland"),
    "GT": Country("GT", "Guatemala"),
    "GF": Country("GF", "French Guiana"),
    "GU": Country("GU", "Guam"),
    "GY": Country("GY", "Guyana"),
    "HK": Country("HK", "Hong Kong"),
    "HM": Country("HM", "Heard Island and McDonald Islands"),
    "HN": Country("HN", "Honduras"),
    "HR": Country("HR", "Croatia"),
    "HT": Country("HT", "Haiti"),
    "HU": Country("HU", "Hungary"),
    "ID": Country("ID", "Indonesia"),
    "IM": Country("IM", "Isle of Man"),
    "IN": Country("IN", "India"),
    "IO": Country("IO", "British Indian Ocean Territory"),
    "IE": Country("IE", "Ireland"),
    "IR": Country("IR", "Iran"),
    "IQ": Country("IQ", "Iraq"),
    "IS": Country("IS", "Iceland"),
    "IL": Country("IL", "Israel"),
    "IT": Country("IT", "Italy"),
    "JM": Country("JM", "Jamaica"),
    "JE": Country("JE", "Jersey"),
    "JO": Country("JO", "Jordan"),
    "JP": Country("JP", "Japan"),
    "KZ": Country("KZ", "Kazakhstan"),
    "KE": Country("KE", "Kenya"),
    "KG": Country("KG", "Kyrgyzstan"),
    "KH": Country("KH", "Cambodia"),
    "KI": Country("KI", "Kiribati"),
    "KN": Country("KN", "Saint Kitts and Nevis"),
    "KR": Country("KR", "South Korea"),
    "KW": Country("KW", "Kuwait"),
    "LA": Country("LA", "Laos"),
    "LB": Country("LB", "Lebanon"),
    "LR": Country("LR", "Liberia"),
    "LY": Country("LY", "Libya"),
    "LC": Country("LC", "Saint Lucia"),
    "LI": Country("LI", "Liechtenstein"),
    "LK": Country("LK", "Sri Lanka"),
    "LS": Country("LS", "Lesotho"),
    "LT": Country("LT", "Lithuania"),
    "LU": Country("LU", "Luxembourg"),
    "LV": Country("LV", "Latvia"),
    "MO": Country("MO", "Macao"),
    "MF": Country("MF", "Saint Martin (French part)"),
    "MA": Country("MA", "Morocco"),
    "MC": Country("MC", "Monaco"),
    "MD": Country("MD", "Moldova"),
    "MG": Country("MG", "Madagascar"),
    "MV": Country("MV", "Maldives"),
    "MX": Country("MX", "Mexico"),
    "MH": Country("MH", "Marshall Islands"),
    "MK": Country("MK", "North Macedonia"),
    "ML": Country("ML", "Mali"),
    "MT": Country("MT", "Malta"),
    "MM": Country("MM", "Myanmar"),
    "ME": Country("ME", "Montenegro"),
    "MN": Country("MN", "Mongolia"),
    "MP": Country("MP", "Northern Mariana Islands"),
    "MZ": Country("MZ", "Mozambique"),
    "MR": Country("MR", "Mauritania"),
    "MS": Country("MS", "Montserrat"),
    "MQ": Country("MQ", "Martinique"),
    "MU": Country("MU", "Mauritius"),
    "MW": Country("MW", "Malawi"),
    "MY": Country("MY", "Malaysia"),
    "YT": Country("YT", "Mayotte"),
    "NA": Country("NA", "Namibia"),
    "NC": Country("NC", "New Caledonia"),
    "NE": Country("NE", "Niger"),
    "NF": Country("NF", "Norfolk Island"),
    "NG": Country("NG", "Nigeria"),
    "NI": Country("NI", "Nicaragua"),
    "NU": Country("NU", "Niue"),
    "NL": Country("NL", "Netherlands"),
    "NO": Country("NO", "Norway"),
    "NP": Country("NP", "Nepal"),
    "NR": Country("NR", "Nauru"),
    "NZ": Country("NZ", "New Zealand"),
    "OM": Country("OM", "Oman"),
    "PK": Country("PK", "Pakistan"),
    "PA": Country("PA", "Panama"),
    "PN": Country("PN", "Pitcairn"),
    "PE": Country("PE", "Peru"),
    "PH": Country("PH", "Philippines"),
    "PW": Country("PW", "Palau"),
    "PG": Country("PG", "Papua New Guinea"),
    "PL": Country("PL", "Poland"),
    "PR": Country("PR", "Puerto Rico"),
    "KP": Country("KP", "North Korea"),
    "PT": Country("PT", "Portugal"),
    "PY": Country("PY", "Paraguay"),
    "PS": Country("PS", "Palestine, State of"),
    "PF": Country("PF", "French Polynesia"),
    "QA": Country("QA", "Qatar"),
    "RE": Country("RE", "Réunion"),
    "RO": Country("RO", "Romania"),
    "RU": Country("RU", "Russian Federation"),
    "RW": Country("RW", "Rwanda"),
    "SA": Country("SA", "Saudi Arabia"),
    "SD": Country("SD", "Sudan"),
    "SN": Country("SN", "Senegal"),
    "SG": Country("SG", "Singapore"),
    "GS": Country("GS", "South Georgia and the South Sandwich Islands"),
    "SH": Country("SH", "Saint Helena, Ascension and Tristan da Cunha"),
    "SJ": Country("SJ", "Svalbard and Jan Mayen"),
    "SB": Country("SB", "Solomon Islands"),
    "SL": Country("SL", "Sierra Leone"),
    "SV": Country("SV", "El Salvador"),
    "SM": Country("SM", "San Marino"),
    "SO": Country("SO", "Somalia"),
    "PM": Country("PM", "Saint Pierre and Miquelon"),
    "RS": Country("RS", "Serbia"),
    "SS": Country("SS", "South Sudan"),
    "ST": Country("ST", "Sao Tome and Principe"),
    "SR": Country("SR", "Suriname"),
    "SK": Country("SK", "Slovakia"),
    "SI": Country("SI", "Slovenia"),
    "SE": Country("SE", "Sweden"),
    "SZ": Country("SZ", "Eswatini"),
    "SX": Country("SX", "Sint Maarten (Dutch part)"),
    "SC": Country("SC", "Seychelles"),
    "SY": Country("SY", "Syria"),
    "TC": Country("TC", "Turks and Caicos Islands"),
    "TD": Country("TD", "Chad"),
    "TG": Country("TG", "Togo"),
    "TH": Country("TH", "Thailand"),
    "TJ": Country("TJ", "Tajikistan"),
    "TK": Country("TK", "Tokelau"),
    "TM": Country("TM", "Turkmenistan"),
    "TL": Country("TL", "Timor-Leste"),
    "TO": Country("TO", "Tonga"),
    "TT": Country("TT", "Trinidad and Tobago"),
    "TN": Country("TN", "Tunisia"),
    "TR": Country("TR", "Türkiye"),
    "TV": Country("TV", "Tuvalu"),
    "TW": Country("TW", "Taiwan"),
    "TZ": Country("TZ", "Tanzania"),
    "UG": Country("UG", "Uganda"),
    "UA": Country("UA", "Ukraine"),
    "UM": Country("UM", "United States Minor Outlying Islands"),
    "UY": Country("UY", "Uruguay"),
    "US": Country("US", "United States"),
    "UZ": Country("UZ", "Uzbekistan"),
    "VA": Country("VA", "Holy See (Vatican City State)"),
    "VC": Country("VC", "Saint Vincent and the Grenadines"),
    "VE": Country("VE", "Venezuela"),
    "VG": Country("VG", "Virgin Islands, British"),
    "VI": Country("VI", "Virgin Islands, U.S."),
    "VN": Country("VN", "Vietnam"),
    "VU": Country("VU", "Vanuatu"),
    "WF": Country("WF", "Wallis and Futuna"),
    "WS": Country("WS", "Samoa"),
    "YE": Country("YE", "Yemen"),
    "ZA": Country("ZA", "South Africa"),
    "ZM": Country("ZM", "Zambia"),
    "ZW": Country("ZW", "Zimbabwe"),
}
