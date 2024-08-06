/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { LocationCreateSchema } from "../../models/location-create-schema";
import { LocationReadSchema } from "../../models/location-read-schema";

export interface CreateLocation$Params {
	body: LocationCreateSchema;
}

export function createLocation(
	http: HttpClient,
	rootUrl: string,
	params: CreateLocation$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<LocationReadSchema>> {
	const rb = new RequestBuilder(rootUrl, createLocation.PATH, "post");
	if (params) {
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

createLocation.PATH = "/api/location/";
