/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { LocationReadSchema } from "../../models/location-read-schema";

export interface GetLocation$Params {
	location_id: number;
}

export function getLocation(
	http: HttpClient,
	rootUrl: string,
	params: GetLocation$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<LocationReadSchema>> {
	const rb = new RequestBuilder(rootUrl, getLocation.PATH, "get");
	if (params) {
		rb.path("location_id", params.location_id, {});
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

getLocation.PATH = "/api/location/{location_id}/";
