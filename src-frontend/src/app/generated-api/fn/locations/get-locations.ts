/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PagedLocationReadSchema } from "../../models/paged-location-read-schema";

export interface GetLocations$Params {
	page?: number;
}

export function getLocations(
	http: HttpClient,
	rootUrl: string,
	params?: GetLocations$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<PagedLocationReadSchema>> {
	const rb = new RequestBuilder(rootUrl, getLocations.PATH, "get");
	if (params) {
		rb.query("page", params.page, {});
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<PagedLocationReadSchema>;
			}),
		);
}

getLocations.PATH = "/api/location/";
