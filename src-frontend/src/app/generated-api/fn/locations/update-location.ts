/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { LocationReadSchema } from "../../models/location-read-schema";
import { LocationUpdateSchema } from "../../models/location-update-schema";

export interface UpdateLocation$Params {
	location_id: number;
	body: LocationUpdateSchema;
}

export function updateLocation(
	http: HttpClient,
	rootUrl: string,
	params: UpdateLocation$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<LocationReadSchema>> {
	const rb = new RequestBuilder(rootUrl, updateLocation.PATH, "patch");
	if (params) {
		rb.path("location_id", params.location_id, {});
		rb.body(params.body, "application/json");
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<LocationReadSchema>;
			}),
		);
}

updateLocation.PATH = "/api/location/{location_id}/";
