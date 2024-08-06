/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PagedPersonReadSchema } from "../../models/paged-person-read-schema";

export interface GetPeople$Params {
	name_like?: string | null;
	page?: number;
}

export function getPeople(
	http: HttpClient,
	rootUrl: string,
	params?: GetPeople$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<PagedPersonReadSchema>> {
	const rb = new RequestBuilder(rootUrl, getPeople.PATH, "get");
	if (params) {
		rb.query("name_like", params.name_like, {});
		rb.query("page", params.page, {});
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<PagedPersonReadSchema>;
			}),
		);
}

getPeople.PATH = "/api/person/";
