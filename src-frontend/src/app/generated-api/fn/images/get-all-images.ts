/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { Pagedint } from "../../models/pagedint";

export interface GetAllImages$Params {
	includes_people?: Array<any> | null;
	excludes_people?: Array<any> | null;
	includes_pets?: Array<any> | null;
	excludes_pets?: Array<any> | null;
	includes_locations?: Array<any> | null;
	excludes_locations?: Array<any> | null;
	page?: number;
}

export function getAllImages(
	http: HttpClient,
	rootUrl: string,
	params?: GetAllImages$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<Pagedint>> {
	const rb = new RequestBuilder(rootUrl, getAllImages.PATH, "get");
	if (params) {
		rb.query("includes_people", params.includes_people, {});
		rb.query("excludes_people", params.excludes_people, {});
		rb.query("includes_pets", params.includes_pets, {});
		rb.query("excludes_pets", params.excludes_pets, {});
		rb.query("includes_locations", params.includes_locations, {});
		rb.query("excludes_locations", params.excludes_locations, {});
		rb.query("page", params.page, {});
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<Pagedint>;
			}),
		);
}

getAllImages.PATH = "/api/image/";
