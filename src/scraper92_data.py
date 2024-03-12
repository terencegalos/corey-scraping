data = {
	"active": False,
	"allow_link": "True",
	"color": "default",
	"color_dv": "Default",
	"css": "\n#x61108f231be6649089df9796bc4bcb22 .panel {\n\tpadding: 0;\n}\n\n#x61108f231be6649089df9796bc4bcb22 .panel-heading .panel-title {\n\tfont-size: 32px;\n\tfont-weight: 300;\n}\n\n#x61108f231be6649089df9796bc4bcb22 .table > thead:first-child > tr:first-child > th {\n\tborder-left: 0;\n}\n\n#x61108f231be6649089df9796bc4bcb22 .panel-heading .dropdown-toggle {\n\tdisplay: none;\n}",
	"d": "desc",
	"display_field": "business_address",
	"enable_filter": "False",
	"fields": "",
	"filter": "status=Published^EQ",
	"headerTitle": "Robocall Mitigation Database",
	"hide_header": False,
	"maximum_entries": 8,
	"o": "sys_updated_on",
	"order": -1,
	"order_by": "sys_updated_on",
	"order_direction": "desc",
	"order_direction_dv": "Descending",
	"roles": "public",
	"sessionRotationTrigger": True,
	"show_attachment_link": "True",
	"show_breadcrumbs": False,
	"show_keywords": "True",
	"size": "md",
	"size_dv": "Medium",
	"sp_column": "a9f394611b566c1048c6ed7bbc4bcba2",
	"sp_column_dv": "",
	"sp_page": "rmd_form",
	"sp_page_dv": "rmd_form",
	"sp_widget": "75af76231be6649089df9796bc4bcbdd",
	"sp_widget_dv": "",
	"sys_class_name": "sp_instance_table",
	"sys_class_name_dv": "Instance with Table",
	"sys_name": "Robocall Mitigation Database",
	"sys_tags": "",
	"table": "x_g_fmc_rmd_robocall_mitigation_database",
	"title": "Robocall Mitigation Database",
	"view": "service_portal",
	"widget_parameters": "{\n\t\"show_keywords\": {\n\t\t\"value\": \"True\",\n\t\t\"displayValue\": \"True\"\n\t},\n\t\"allow_link\": {\n\t\t\"value\": \"True\",\n\t\t\"displayValue\": \"True\"\n\t},\n\t\"view\": {\n\t\t\"value\": \"service_portal\",\n\t\t\"displayValue\": \"service_portal\"\n\t},\n\t\"show_attachment_link\": {\n\t\t\"value\": \"True\",\n\t\t\"displayValue\": \"True\"\n\t},\n\t\"show_breadcrumbs\": {\n\t\t\"value\": False,\n\t\t\"displayValue\": False\n\t},\n\t\"hide_header\": {\n\t\t\"value\": False,\n\t\t\"displayValue\": False\n\t}\n}",
	"window_size": "8",
    "p":2
}



data02 = {
	"active": False,
	"allow_link": "True",
	"canCreate": False,
	"color": "default",
	"color_dv": "Default",
	"column_labels": {
		"business_address": "Business Address",
		"business_name": "Business Name",
		"contact_business_address": "Contact Business Address",
		"contact_department": "Contact Department",
		"contact_telephone_number": "Contact Telephone Number",
		"contact_title": "Contact Title",
		"foreign_voice_provider": "Foreign Voice Service Provider",
		"frn": "FCC Registration Number (FRN)",
		"gateway_provider_choice": "Gateway Provider",
		"implementation": "Implementation",
		"intermediate_provider_choice": "Non-Gateway Intermediate Provider",
		"other_dba_names": "Other DBA Name(s)",
		"pdf": "PDF",
		"previous_dba_names": "Previous Business Names",
		"robocall_mitigation_contact_name": "Robocall Mitigation Contact Name",
		"voice_service_provider_choice": "Voice Service Provider"
	},
	"column_types": {
		"business_address": "string",
		"business_name": "string",
		"contact_business_address": "string",
		"contact_department": "string",
		"contact_telephone_number": "string",
		"contact_title": "string",
		"foreign_voice_provider": "string",
		"frn": "reference",
		"gateway_provider_choice": "string",
		"implementation": "string",
		"intermediate_provider_choice": "string",
		"other_dba_names": "string",
		"pdf": "file_attachment",
		"previous_dba_names": "string",
		"robocall_mitigation_contact_name": "string",
		"voice_service_provider_choice": "string"
	},
	"css": "\n#x61108f231be6649089df9796bc4bcb22 .panel {\n\tpadding: 0;\n}\n\n#x61108f231be6649089df9796bc4bcb22 .panel-heading .panel-title {\n\tfont-size: 32px;\n\tfont-weight: 300;\n}\n\n#x61108f231be6649089df9796bc4bcb22 .table > thead:first-child > tr:first-child > th {\n\tborder-left: 0;\n}\n\n#x61108f231be6649089df9796bc4bcb22 .panel-heading .dropdown-toggle {\n\tdisplay: none;\n}",
	"d": "desc",
	"display_field": "business_address",
	"enable_filter": False,
	"exportQuery": "status=Published",
	"exportQueryEncoded": "status%3DPublished",
	"fields": "business_name,frn,previous_dba_names,business_address,other_dba_names,foreign_voice_provider,implementation,voice_service_provider_choice,gateway_provider_choice,intermediate_provider_choice,robocall_mitigation_contact_name,contact_title,contact_department,contact_business_address,contact_telephone_number,pdf",
	"fields_array": [
		"business_name",
		"frn",
		"previous_dba_names",
		"business_address",
		"other_dba_names",
		"foreign_voice_provider",
		"implementation",
		"voice_service_provider_choice",
		"gateway_provider_choice",
		"intermediate_provider_choice",
		"robocall_mitigation_contact_name",
		"contact_title",
		"contact_department",
		"contact_business_address",
		"contact_telephone_number",
		"pdf"
	],
	"filter": "status=Published",
	"filterBreadcrumbs": {
		"_server_time": "0.004",
		"client_script": "function ($scope, $timeout, $element){\n\tvar eventNames = {\n\t\tsetBreadcrumbs: 'widget-filter-breadcrumbs.setBreadcrumbs'\n\t};\n\t$scope.adjustFilter = function(breadcrumb, remove){\n\t\tvar newQuery = remove ? breadcrumb.ifRemoved : breadcrumb.value;\n\t\t$scope.$emit('widget-filter-breadcrumbs.queryModified', newQuery);\n\t}\n\t$scope.$on(eventNames.setBreadcrumbs, function(e, data, newQuery){\n\t\t$scope.data = data;\n\t\t$scope.$broadcast(\"snfilter:initialize_query\", massageEncodedQuery(newQuery));\n\t});\n\t$scope.clickFilter = function() {\n\t\t$scope.showFilter = !$scope.showFilter;\n\t\t$scope.filterMsg = $scope.showFilter ? $scope.data.hideMsg: $scope.data.showMsg;\n\t}\n\t$scope.showFilter = False;\n\t$scope.filterMsg = $scope.data.showMsg;\n\t$scope.$on(\"snbreadcrumbs:toggle_filter\", function(e) {\n\t\te.stopPropagation();\n\t\te.preventDefault();\n\t\t$scope.showFilter = False;\n\t\t$scope.filterMsg = $scope.data.showMsg;\n\t\t$element.find('#filterToggle').focus();\n\t\t\n\t});\n\t$scope.$on(\"snfilter:update_query\", function(e, query) {\n\t\te.stopPropagation();\n\t\te.preventDefault();\n\t\t$scope.$emit('widget-filter-breadcrumbs.queryModified', massageEncodedQuery(query));\n\t\t$scope.showFilter = False;\n\t\t$scope.filterMsg = $scope.data.showMsg;\n\t});\n\t$scope.$on(\"snfilter:run_filter\", function(e) {\n\t\t$element.find('#filterToggle').focus();\n\t});\n\tfunction massageEncodedQuery(query) {\nreturn (query) ? query.replace(/CONTAINS/g, \"LIKE\").replace(/DOES NOT CONTAIN/g, \"NOT LIKE\") : query;\n\t}\n}\n",
		"controller_as": "",
		"css": "\n.v339a5c41d7201200b0b044580e61030d .breadcrumbs {\n\tmargin-left: 9px;\n\tmargin-bottom: 3px;\n}\n\n.v339a5c41d7201200b0b044580e61030d .icon-filter {\n\tfont-size: 20px;\n\ttext-decoration: inherit;\n}\n\n.v339a5c41d7201200b0b044580e61030d .ng-filter-widget {\n\tposition: static;\n}\n\n.v339a5c41d7201200b0b044580e61030d .ng-filter-widget .modal .manage-filters-button {\n\ttop: 15px;\n}\n\n.v339a5c41d7201200b0b044580e61030d .ng-filter-widget .modal .input-group-radio input {\n\tmargin-left: 0;\n}\n\n.v339a5c41d7201200b0b044580e61030d .ng-filter-widget .modal .input-group-transparent {\n\tposition: relative;\n}\n\n.v339a5c41d7201200b0b044580e61030d .ng-filter-widget .modal .input-group-transparent .input-group-addon-transparent {\n\tposition: absolute;\n\tfont-size: 18px;\n\ttop: 2px;\n\tleft: 8px;\n}\n\n.v339a5c41d7201200b0b044580e61030d .ng-filter-widget .modal .input-group-transparent input {\n\tborder-radius: 9999px;\n\tpadding-left: 28px;\n}\n\n.v339a5c41d7201200b0b044580e61030d .ng-filter-widget .modal ul {\n\tpadding: 0 5px 10px;\n}\n\n.v339a5c41d7201200b0b044580e61030d .ng-filter-widget .modal ul li button {\n\tbackground-color: inherit;\n}\n\n.v339a5c41d7201200b0b044580e61030d .ng-filter-widget .modal ul li a {\n\twidth: 100%;\n\toverflow: hidden;\n\ttext-overflow: ellipsis;\n\twhite-space: nowrap;\n\tdisplay: block;\n\tpadding: 7px 20px;\n\ttext-decoration: none;\n\tcursor: pointer;\n}",
		"data": {
			"breadcrumbs": [
				{
					"ifRemoved": "",
					"isFixed": False,
					"label": "All",
					"value": ""
				},
				{
					"ifRemoved": "",
					"isFixed": False,
					"label": "Status = Published",
					"value": "status=Published"
				}
			],
			"enable_filter": False,
			"hideMsg": "Hide filter",
			"showMsg": "Show filter"
		},
		"dependencies": [],
		"field_list": "",
		"id": "widget-filter-breadcrumbs",
		"name": "Filter Breadcrumbs",
		"option_schema": "[{\"hint\":\"Table to be used to generate breadcrumbs\",\"name\":\"table\",\"section\":\"Data\",\"label\":\"Table\",\"type\":\"string\"},{\"name\":\"query\",\"section\":\"Data\",\"label\":\"Query\",\"type\":\"string\"},{\"hint\":\"If enabled, a filter button prompt will be added to the breadcrumb list\",\"name\":\"enable_filter\",\"default_value\":\"False\",\"section\":\"Behavior\",\"label\":\"Enable Filter\",\"type\":\"boolean\"}]",
		"options": {
			"active": False,
			"enable_filter": False,
			"order": -1,
			"query": "status=Published",
			"sp_column_dv": "",
			"sp_widget_dv": "",
			"sys_tags": "",
			"table": "x_g_fmc_rmd_robocall_mitigation_database"
		},
		"providers": [],
		"public": True,
		"roles": "",
		"sys_class_name": "sp_widget",
		"sys_id": "339a5c41d7201200b0b044580e61030d",
		"sys_scope": "global",
		"template": "<div class=\"breadcrumbs\"> \n <button type=\"button\" role=\"button\" id=\"filterToggle\" ng-show=\"data.enable_filter\" ng-click=\"clickFilter()\" title=\"{{filterMsg}}\" class=\"icon-filter btn btn-link\" tabindex=\"0\" data-original-title=\"{{filterMsg}}\" aria-expanded=\"{{showFilter}}\"><span class=\"sr-only\">{{filterMsg}}</span></button> \n <span ng-repeat=\"crumb in data.breadcrumbs track by crumb.value\"> <a href=\"javascript:void(0)\" ng-if=\"!$first\" class=\"sp-breadcrumb-link sp-breadcrumb-remove-condition\" ng-click=\"adjustFilter(crumb, True)\" aria-label=\"Remove next condition {{crumb.label}}\" title=\"Remove next condition\" data-toggle=\"tooltip\" data-placement=\"bottom\">&gt;</a> <a href=\"javascript:void(0)\" class=\"sp-breadcrumb-link\" ng-click=\"adjustFilter(crumb, False)\">{{crumb.label}}</a> </span> \n</div>\n<div ng-if=\"data.enable_filter\"> \n <span ng-show=\"showFilter\"> \n  <sp-widget widget=\"data.filterWidget\"></sp-widget> </span> \n</div>"
	},
	"hasTextIndex": True,
	"headerTitle": "Robocall Mitigation Database",
	"hide_header": False,
	"inputMax": 4,
	"inputSize": 2,
	"keywords": "",
	"list": [
		{
			"business_address": {
				"display_value": "445 Broadhollow Road\nSuite 25\nMelville NY 11747",
				"label": "Business Address",
				"type": "string",
				"value": "445 Broadhollow Road\nSuite 25\nMelville NY 11747"
			},
			"business_name": {
				"display_value": "Tricom Technology Inc",
				"label": "Business Name",
				"limit": "40",
				"type": "string",
				"value": "Tricom Technology Inc"
			},
			"contact_business_address": {
				"display_value": "445 Broad Hollow Road\nSuite 25\nMelville NY 11747",
				"label": "Contact Business Address",
				"limit": "40",
				"type": "string",
				"value": "445 Broad Hollow Road\nSuite 25\nMelville NY 11747"
			},
			"contact_department": {
				"display_value": "Sales",
				"label": "Contact Department",
				"limit": "40",
				"type": "string",
				"value": "Sales"
			},
			"contact_telephone_number": {
				"display_value": "+15166948100",
				"label": "Contact Telephone Number",
				"limit": "40",
				"type": "string",
				"value": "+15166948100"
			},
			"contact_title": {
				"display_value": "President",
				"label": "Contact Title",
				"limit": "40",
				"type": "string",
				"value": "President"
			},
			"foreign_voice_provider": {
				"display_value": "No",
				"label": "Foreign Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"frn": {
				"display_value": "0026495937",
				"label": "FCC Registration Number (FRN)",
				"limit": "40",
				"type": "reference",
				"value": "4fdace191b388250b68ea828624bcb0a"
			},
			"gateway_provider_choice": {
				"display_value": "No",
				"label": "Gateway Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"implementation": {
				"display_value": "Complete STIR/SHAKEN Implementation",
				"label": "Implementation",
				"type": "string",
				"value": "Complete STIR/SHAKEN Implementation"
			},
			"intermediate_provider_choice": {
				"display_value": "No",
				"label": "Non-Gateway Intermediate Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"other_dba_names": {
				"display_value": "None",
				"label": "Other DBA Name(s)",
				"limit": "40",
				"type": "string",
				"value": "None"
			},
			"pdf": {
				"display_value": "Tricom Technology Robocall Mitigation Compliance.pdf",
				"label": "PDF",
				"limit": "40",
				"type": "file_attachment",
				"value": "1535d6111b788250b68ea828624bcbe0"
			},
			"previous_dba_names": {
				"display_value": "None",
				"label": "Previous Business Names",
				"limit": "40",
				"type": "string",
				"value": "None"
			},
			"robocall_mitigation_contact_name": {
				"display_value": "Frank Rubiano",
				"label": "Robocall Mitigation Contact Name",
				"limit": "40",
				"type": "string",
				"value": "Frank Rubiano"
			},
			"sys_id": "5e4ec6d91b388250b68ea828624bcb77",
			"targetTable": "x_g_fmc_rmd_robocall_mitigation_database",
			"voice_service_provider_choice": {
				"display_value": "Yes",
				"label": "Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "Yes"
			}
		},
		{
			"business_address": {
				"display_value": "4995 NW 72 Avenue Suite #306\nMiami FL 33166",
				"label": "Business Address",
				"type": "string",
				"value": "4995 NW 72 Avenue Suite #306\nMiami FL 33166"
			},
			"business_name": {
				"display_value": "Excelsior Labs Inc",
				"label": "Business Name",
				"limit": "40",
				"type": "string",
				"value": "Excelsior Labs Inc"
			},
			"contact_business_address": {
				"display_value": "N/A",
				"label": "Contact Business Address",
				"limit": "40",
				"type": "string",
				"value": "N/A"
			},
			"contact_department": {
				"display_value": "Management",
				"label": "Contact Department",
				"limit": "40",
				"type": "string",
				"value": "Management"
			},
			"contact_telephone_number": {
				"display_value": "7864613878",
				"label": "Contact Telephone Number",
				"limit": "40",
				"type": "string",
				"value": "7864613878"
			},
			"contact_title": {
				"display_value": "CEO",
				"label": "Contact Title",
				"limit": "40",
				"type": "string",
				"value": "CEO"
			},
			"foreign_voice_provider": {
				"display_value": "No",
				"label": "Foreign Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"frn": {
				"display_value": "0033924242",
				"label": "FCC Registration Number (FRN)",
				"limit": "40",
				"type": "reference",
				"value": "0f8d24521b2f25103c7943bae54bcbdf"
			},
			"gateway_provider_choice": {
				"display_value": "No",
				"label": "Gateway Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"implementation": {
				"display_value": "Complete STIR/SHAKEN Implementation",
				"label": "Implementation",
				"type": "string",
				"value": "Complete STIR/SHAKEN Implementation"
			},
			"intermediate_provider_choice": {
				"display_value": "Yes",
				"label": "Non-Gateway Intermediate Provider",
				"limit": "40",
				"type": "string",
				"value": "Yes"
			},
			"other_dba_names": {
				"display_value": "None",
				"label": "Other DBA Name(s)",
				"limit": "40",
				"type": "string",
				"value": "None"
			},
			"pdf": {
				"display_value": "Robocall_Mitigation_Database.pdf",
				"label": "PDF",
				"limit": "40",
				"type": "file_attachment",
				"value": "33741ed91b3c8250d9b4caa8624bcb58"
			},
			"previous_dba_names": {
				"display_value": "None",
				"label": "Previous Business Names",
				"limit": "40",
				"type": "string",
				"value": "None"
			},
			"robocall_mitigation_contact_name": {
				"display_value": "Rafael J Aponte",
				"label": "Robocall Mitigation Contact Name",
				"limit": "40",
				"type": "string",
				"value": "Rafael J Aponte"
			},
			"sys_id": "8bade8521b23651085edebdbac4bcb5a",
			"targetTable": "x_g_fmc_rmd_robocall_mitigation_database",
			"voice_service_provider_choice": {
				"display_value": "No",
				"label": "Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			}
		},
		{
			"business_address": {
				"display_value": "22555 Hillside Circle\nLeesburg VA 20175",
				"label": "Business Address",
				"type": "string",
				"value": "22555 Hillside Circle\nLeesburg VA 20175"
			},
			"business_name": {
				"display_value": "Telspace Solutions,LLC",
				"label": "Business Name",
				"limit": "40",
				"type": "string",
				"value": "Telspace Solutions,LLC"
			},
			"contact_business_address": {
				"display_value": "22555  Hillside Circle\nLeesburg VA 20175",
				"label": "Contact Business Address",
				"limit": "40",
				"type": "string",
				"value": "22555  Hillside Circle\nLeesburg VA 20175"
			},
			"contact_department": {
				"display_value": "Service",
				"label": "Contact Department",
				"limit": "40",
				"type": "string",
				"value": "Service"
			},
			"contact_telephone_number": {
				"display_value": "3016513779",
				"label": "Contact Telephone Number",
				"limit": "40",
				"type": "string",
				"value": "3016513779"
			},
			"contact_title": {
				"display_value": "PM",
				"label": "Contact Title",
				"limit": "40",
				"type": "string",
				"value": "PM"
			},
			"foreign_voice_provider": {
				"display_value": "No",
				"label": "Foreign Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"frn": {
				"display_value": "0035008325",
				"label": "FCC Registration Number (FRN)",
				"limit": "40",
				"type": "reference",
				"value": "5d8f824fdbe00e10bf8e1b58139619b6"
			},
			"gateway_provider_choice": {
				"display_value": "No",
				"label": "Gateway Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"implementation": {
				"display_value": "Complete STIR/SHAKEN Implementation",
				"label": "Implementation",
				"type": "string",
				"value": "Complete STIR/SHAKEN Implementation"
			},
			"intermediate_provider_choice": {
				"display_value": "No",
				"label": "Non-Gateway Intermediate Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"other_dba_names": {
				"display_value": "NONE",
				"label": "Other DBA Name(s)",
				"limit": "40",
				"type": "string",
				"value": "NONE"
			},
			"pdf": {
				"display_value": "TSRoboCall.pdf",
				"label": "PDF",
				"limit": "40",
				"type": "file_attachment",
				"value": "33241add1b388250b68ea828624bcb19"
			},
			"previous_dba_names": {
				"display_value": "NONE",
				"label": "Previous Business Names",
				"limit": "40",
				"type": "string",
				"value": "NONE"
			},
			"robocall_mitigation_contact_name": {
				"display_value": "Bill Terry",
				"label": "Robocall Mitigation Contact Name",
				"limit": "40",
				"type": "string",
				"value": "Bill Terry"
			},
			"sys_id": "5083d2dd1b388250b68ea828624bcb4c",
			"targetTable": "x_g_fmc_rmd_robocall_mitigation_database",
			"voice_service_provider_choice": {
				"display_value": "Yes",
				"label": "Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "Yes"
			}
		},
		{
			"business_address": {
				"display_value": "1280 E. Highway 76\nSTE G\nBRANSON MO 65616",
				"label": "Business Address",
				"type": "string",
				"value": "1280 E. Highway 76\nSTE G\nBRANSON MO 65616"
			},
			"business_name": {
				"display_value": "VANDERLINK",
				"label": "Business Name",
				"limit": "40",
				"type": "string",
				"value": "VANDERLINK"
			},
			"contact_business_address": {
				"display_value": "1280 E. State Highway 76\nSTEG\nBranson MO 65616",
				"label": "Contact Business Address",
				"limit": "40",
				"type": "string",
				"value": "1280 E. State Highway 76\nSTEG\nBranson MO 65616"
			},
			"contact_department": {
				"display_value": "CEO",
				"label": "Contact Department",
				"limit": "40",
				"type": "string",
				"value": "CEO"
			},
			"contact_telephone_number": {
				"display_value": "417-266-5656",
				"label": "Contact Telephone Number",
				"limit": "40",
				"type": "string",
				"value": "417-266-5656"
			},
			"contact_title": {
				"display_value": "CEO",
				"label": "Contact Title",
				"limit": "40",
				"type": "string",
				"value": "CEO"
			},
			"foreign_voice_provider": {
				"display_value": "No",
				"label": "Foreign Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"frn": {
				"display_value": "0024422578",
				"label": "FCC Registration Number (FRN)",
				"limit": "40",
				"type": "reference",
				"value": "a3151ab21b6451509294113d9c4bcb2b"
			},
			"gateway_provider_choice": {
				"display_value": "No",
				"label": "Gateway Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"implementation": {
				"display_value": "No STIR/SHAKEN Implementation - Performing Robocall Mitigation",
				"label": "Implementation",
				"type": "string",
				"value": "No STIR/SHAKEN Implementation - Performing Robocall Mitigation"
			},
			"intermediate_provider_choice": {
				"display_value": "No",
				"label": "Non-Gateway Intermediate Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"other_dba_names": {
				"display_value": "NONE",
				"label": "Other DBA Name(s)",
				"limit": "40",
				"type": "string",
				"value": "NONE"
			},
			"pdf": {
				"display_value": "Robocall Mitigation Plan-Reseller of Skyswitch 2024 new.pdf",
				"label": "PDF",
				"limit": "40",
				"type": "file_attachment",
				"value": "1ffbca1187748250467d0ed8cebb355f"
			},
			"previous_dba_names": {
				"display_value": "NONE",
				"label": "Previous Business Names",
				"limit": "40",
				"type": "string",
				"value": "NONE"
			},
			"robocall_mitigation_contact_name": {
				"display_value": "Garrett Vanderpool",
				"label": "Robocall Mitigation Contact Name",
				"limit": "40",
				"type": "string",
				"value": "Garrett Vanderpool"
			},
			"sys_id": "9f7a0add87348250467d0ed8cebb358f",
			"targetTable": "x_g_fmc_rmd_robocall_mitigation_database",
			"voice_service_provider_choice": {
				"display_value": "Yes",
				"label": "Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "Yes"
			}
		},
		{
			"business_address": {
				"display_value": "500 N. Akard\nRoss Towers, Suite 3475\nDallas TX 75201",
				"label": "Business Address",
				"type": "string",
				"value": "500 N. Akard\nRoss Towers, Suite 3475\nDallas TX 75201"
			},
			"business_name": {
				"display_value": "Zoom Online Group LLC",
				"label": "Business Name",
				"limit": "40",
				"type": "string",
				"value": "Zoom Online Group LLC"
			},
			"contact_business_address": {
				"display_value": "500 N. Akard\nRoss Towers, Suite 3475\nDallas TX 75201",
				"label": "Contact Business Address",
				"limit": "40",
				"type": "string",
				"value": "500 N. Akard\nRoss Towers, Suite 3475\nDallas TX 75201"
			},
			"contact_department": {
				"display_value": "Compliance",
				"label": "Contact Department",
				"limit": "40",
				"type": "string",
				"value": "Compliance"
			},
			"contact_telephone_number": {
				"display_value": "(602) 576-5150",
				"label": "Contact Telephone Number",
				"limit": "40",
				"type": "string",
				"value": "(602) 576-5150"
			},
			"contact_title": {
				"display_value": "Principal",
				"label": "Contact Title",
				"limit": "40",
				"type": "string",
				"value": "Principal"
			},
			"foreign_voice_provider": {
				"display_value": "No",
				"label": "Foreign Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"frn": {
				"display_value": "0034851568",
				"label": "FCC Registration Number (FRN)",
				"limit": "40",
				"type": "reference",
				"value": "0a370a95dbb88250759ca25813961925"
			},
			"gateway_provider_choice": {
				"display_value": "No",
				"label": "Gateway Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"implementation": {
				"display_value": "No STIR/SHAKEN Implementation - Performing Robocall Mitigation",
				"label": "Implementation",
				"type": "string",
				"value": "No STIR/SHAKEN Implementation - Performing Robocall Mitigation"
			},
			"intermediate_provider_choice": {
				"display_value": "No",
				"label": "Non-Gateway Intermediate Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"other_dba_names": {
				"display_value": "Zoom Online",
				"label": "Other DBA Name(s)",
				"limit": "40",
				"type": "string",
				"value": "Zoom Online"
			},
			"pdf": {
				"display_value": "ROBOCALL MITIGATION PROGRAM_ZOOMONLINE_02-17-2024.pdf",
				"label": "PDF",
				"limit": "40",
				"type": "file_attachment",
				"value": "b81b0e591b7006500073edf7624bcb72"
			},
			"previous_dba_names": {
				"display_value": "None",
				"label": "Previous Business Names",
				"limit": "40",
				"type": "string",
				"value": "None"
			},
			"robocall_mitigation_contact_name": {
				"display_value": "Wayne D'sa",
				"label": "Robocall Mitigation Contact Name",
				"limit": "40",
				"type": "string",
				"value": "Wayne D'sa"
			},
			"sys_id": "5e574a551b7006500073edf7624bcbef",
			"targetTable": "x_g_fmc_rmd_robocall_mitigation_database",
			"voice_service_provider_choice": {
				"display_value": "Yes",
				"label": "Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "Yes"
			}
		},
		{
			"business_address": {
				"display_value": "6100 Mountain Vista St\nSte 100\nHenderson NV 89014",
				"label": "Business Address",
				"type": "string",
				"value": "6100 Mountain Vista St\nSte 100\nHenderson NV 89014"
			},
			"business_name": {
				"display_value": "Stimulus Technologies Corp",
				"label": "Business Name",
				"limit": "40",
				"type": "string",
				"value": "Stimulus Technologies Corp"
			},
			"contact_business_address": {
				"display_value": "6100 Mountain Vista St\nSte 100\nHenderson NV 89014",
				"label": "Contact Business Address",
				"limit": "40",
				"type": "string",
				"value": "6100 Mountain Vista St\nSte 100\nHenderson NV 89014"
			},
			"contact_department": {
				"display_value": "VoIP",
				"label": "Contact Department",
				"limit": "40",
				"type": "string",
				"value": "VoIP"
			},
			"contact_telephone_number": {
				"display_value": "7025643166",
				"label": "Contact Telephone Number",
				"limit": "40",
				"type": "string",
				"value": "7025643166"
			},
			"contact_title": {
				"display_value": "VoIP Systems Administrator",
				"label": "Contact Title",
				"limit": "40",
				"type": "string",
				"value": "VoIP Systems Administrator"
			},
			"foreign_voice_provider": {
				"display_value": "No",
				"label": "Foreign Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"frn": {
				"display_value": "0034394833",
				"label": "FCC Registration Number (FRN)",
				"limit": "40",
				"type": "reference",
				"value": "88b08345db644610759ca2581396194d"
			},
			"gateway_provider_choice": {
				"display_value": "No",
				"label": "Gateway Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"implementation": {
				"display_value": "Partial STIR/SHAKEN Implementation - Performing Robocall Mitigation",
				"label": "Implementation",
				"type": "string",
				"value": "Partial STIR/SHAKEN Implementation - Performing Robocall Mitigation"
			},
			"intermediate_provider_choice": {
				"display_value": "No",
				"label": "Non-Gateway Intermediate Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"other_dba_names": {
				"display_value": "Stimulus Technologies",
				"label": "Other DBA Name(s)",
				"limit": "40",
				"type": "string",
				"value": "Stimulus Technologies"
			},
			"pdf": {
				"display_value": "Robocall Mitigation Plan.pdf",
				"label": "PDF",
				"limit": "40",
				"type": "file_attachment",
				"value": "e086ca551b388250b68ea828624bcb3a"
			},
			"previous_dba_names": {
				"display_value": "None",
				"label": "Previous Business Names",
				"limit": "40",
				"type": "string",
				"value": "None"
			},
			"robocall_mitigation_contact_name": {
				"display_value": "Richard Cook",
				"label": "Robocall Mitigation Contact Name",
				"limit": "40",
				"type": "string",
				"value": "Richard Cook"
			},
			"sys_id": "dbd54ed11b388250b68ea828624bcba2",
			"targetTable": "x_g_fmc_rmd_robocall_mitigation_database",
			"voice_service_provider_choice": {
				"display_value": "Yes",
				"label": "Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "Yes"
			}
		},
		{
			"business_address": {
				"display_value": "6100 Mountain Vista St. Ste 100\nHenderson NV 89014",
				"label": "Business Address",
				"type": "string",
				"value": "6100 Mountain Vista St. Ste 100\nHenderson NV 89014"
			},
			"business_name": {
				"display_value": "Stimulus Technologies of Oregon, LLC",
				"label": "Business Name",
				"limit": "40",
				"type": "string",
				"value": "Stimulus Technologies of Oregon, LLC"
			},
			"contact_business_address": {
				"display_value": "6100 Mountain Vista St\nSte 100\nHenderson NV 89014",
				"label": "Contact Business Address",
				"limit": "40",
				"type": "string",
				"value": "6100 Mountain Vista St\nSte 100\nHenderson NV 89014"
			},
			"contact_department": {
				"display_value": "VoIP",
				"label": "Contact Department",
				"limit": "40",
				"type": "string",
				"value": "VoIP"
			},
			"contact_telephone_number": {
				"display_value": "7025643166",
				"label": "Contact Telephone Number",
				"limit": "40",
				"type": "string",
				"value": "7025643166"
			},
			"contact_title": {
				"display_value": "VoIP Systems Administrator",
				"label": "Contact Title",
				"limit": "40",
				"type": "string",
				"value": "VoIP Systems Administrator"
			},
			"foreign_voice_provider": {
				"display_value": "No",
				"label": "Foreign Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"frn": {
				"display_value": "0034057778",
				"label": "FCC Registration Number (FRN)",
				"limit": "40",
				"type": "reference",
				"value": "8cb08345db644610759ca2581396194b"
			},
			"gateway_provider_choice": {
				"display_value": "No",
				"label": "Gateway Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"implementation": {
				"display_value": "Partial STIR/SHAKEN Implementation - Performing Robocall Mitigation",
				"label": "Implementation",
				"type": "string",
				"value": "Partial STIR/SHAKEN Implementation - Performing Robocall Mitigation"
			},
			"intermediate_provider_choice": {
				"display_value": "No",
				"label": "Non-Gateway Intermediate Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"other_dba_names": {
				"display_value": "Stimulus Technologies\r\nFireServe Broadband",
				"label": "Other DBA Name(s)",
				"limit": "40",
				"type": "string",
				"value": "Stimulus Technologies\r\nFireServe Broadband"
			},
			"pdf": {
				"display_value": "Robocall Mitigation Plan.pdf",
				"label": "PDF",
				"limit": "40",
				"type": "file_attachment",
				"value": "dc644a151b388250b68ea828624bcb23"
			},
			"previous_dba_names": {
				"display_value": "None",
				"label": "Previous Business Names",
				"limit": "40",
				"type": "string",
				"value": "None"
			},
			"robocall_mitigation_contact_name": {
				"display_value": "Richard Cook",
				"label": "Robocall Mitigation Contact Name",
				"limit": "40",
				"type": "string",
				"value": "Richard Cook"
			},
			"sys_id": "54110a911b388250b68ea828624bcbe3",
			"targetTable": "x_g_fmc_rmd_robocall_mitigation_database",
			"voice_service_provider_choice": {
				"display_value": "Yes",
				"label": "Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "Yes"
			}
		},
		{
			"business_address": {
				"display_value": "401 16th Street N\nSaint Petersburg FL 33705",
				"label": "Business Address",
				"type": "string",
				"value": "401 16th Street N\nSaint Petersburg FL 33705"
			},
			"business_name": {
				"display_value": "Viirtue LLC",
				"label": "Business Name",
				"limit": "40",
				"type": "string",
				"value": "Viirtue LLC"
			},
			"contact_business_address": {
				"display_value": "401 16th Street N\nSaint Petersburg FL 33705",
				"label": "Contact Business Address",
				"limit": "40",
				"type": "string",
				"value": "401 16th Street N\nSaint Petersburg FL 33705"
			},
			"contact_department": {
				"display_value": "Administrative",
				"label": "Contact Department",
				"limit": "40",
				"type": "string",
				"value": "Administrative"
			},
			"contact_telephone_number": {
				"display_value": "8133241000",
				"label": "Contact Telephone Number",
				"limit": "40",
				"type": "string",
				"value": "8133241000"
			},
			"contact_title": {
				"display_value": "President",
				"label": "Contact Title",
				"limit": "40",
				"type": "string",
				"value": "President"
			},
			"foreign_voice_provider": {
				"display_value": "No",
				"label": "Foreign Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"frn": {
				"display_value": "0027109412",
				"label": "FCC Registration Number (FRN)",
				"limit": "40",
				"type": "reference",
				"value": "f2ab31fb1b4170509294113d9c4bcb7e"
			},
			"gateway_provider_choice": {
				"display_value": "No",
				"label": "Gateway Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"implementation": {
				"display_value": "Complete STIR/SHAKEN Implementation",
				"label": "Implementation",
				"type": "string",
				"value": "Complete STIR/SHAKEN Implementation"
			},
			"intermediate_provider_choice": {
				"display_value": "No",
				"label": "Non-Gateway Intermediate Provider",
				"limit": "40",
				"type": "string",
				"value": "No"
			},
			"other_dba_names": {
				"display_value": "Viirtue Inc",
				"label": "Other DBA Name(s)",
				"limit": "40",
				"type": "string",
				"value": "Viirtue Inc"
			},
			"pdf": {
				"display_value": "Viirtue_RCM_March 6 2024.pdf",
				"label": "PDF",
				"limit": "40",
				"type": "file_attachment",
				"value": "894ba1d11b30429048ce5395624bcb64"
			},
			"previous_dba_names": {
				"display_value": "NONE",
				"label": "Previous Business Names",
				"limit": "40",
				"type": "string",
				"value": "NONE"
			},
			"robocall_mitigation_contact_name": {
				"display_value": "Robert Finch",
				"label": "Robocall Mitigation Contact Name",
				"limit": "40",
				"type": "string",
				"value": "Robert Finch"
			},
			"sys_id": "3d36c02a1b963410e560873fe54bcb34",
			"targetTable": "x_g_fmc_rmd_robocall_mitigation_database",
			"voice_service_provider_choice": {
				"display_value": "Yes",
				"label": "Voice Service Provider",
				"limit": "40",
				"type": "string",
				"value": "Yes"
			}
		}
	],
	"maximum_entries": 8,
	"msg": {
		"sortingByAsc": "Sorting by ascending",
		"sortingByDesc": "Sorting by descending"
	},
	"newButtonUnsupported": False,
	"num_pages": 1092,
	"o": "sys_updated_on",
	"order": -1,
	"order_by": "sys_updated_on",
	"order_direction": "desc",
	"order_direction_dv": "Descending",
	"p": 2,
	"page_index": 0,
	"roles": "public",
	"row_count": 8731,
	"sessionRotationTrigger": True,
	"show_attachment_link": "True",
	"show_breadcrumbs": False,
	"show_keywords": "True",
	"size": "md",
	"size_dv": "Medium",
	"sp_column": "a9f394611b566c1048c6ed7bbc4bcba2",
	"sp_column_dv": "",
	"sp_page": "rmd_form",
	"sp_page_dv": "rmd_form",
	"sp_widget": "75af76231be6649089df9796bc4bcbdd",
	"sp_widget_dv": "",
	"sys_class_name": "sp_instance_table",
	"sys_class_name_dv": "Instance with Table",
	"sys_name": "Robocall Mitigation Database",
	"sys_tags": "",
	"table": "x_g_fmc_rmd_robocall_mitigation_database",
	"table_label": "Robocall Mitigation Database",
	"table_plural": "Robocall Mitigation Databases",
	"title": "Robocall Mitigation Database",
	"view": "service_portal",
	"widget_parameters": "{\n\t\"show_keywords\": {\n\t\t\"value\": \"True\",\n\t\t\"displayValue\": \"True\"\n\t},\n\t\"allow_link\": {\n\t\t\"value\": \"True\",\n\t\t\"displayValue\": \"True\"\n\t},\n\t\"view\": {\n\t\t\"value\": \"service_portal\",\n\t\t\"displayValue\": \"service_portal\"\n\t},\n\t\"show_attachment_link\": {\n\t\t\"value\": \"True\",\n\t\t\"displayValue\": \"True\"\n\t},\n\t\"show_breadcrumbs\": {\n\t\t\"value\": False,\n\t\t\"displayValue\": False\n\t},\n\t\"hide_header\": {\n\t\t\"value\": False,\n\t\t\"displayValue\": False\n\t}\n}",
	"window_end": 8,
	"window_size": 8,
	"window_start": 0
}