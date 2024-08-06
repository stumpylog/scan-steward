/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PagedTagRead } from "../../models/paged-tag-read";

export interface GetAllTags$Params {
	page?: number;
}

export function getAllTags(
	http: HttpClient,
	rootUrl: string,
	params?: GetAllTags$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<PagedTagRead>> {
	const rb = new RequestBuilder(rootUrl, getAllTags.PATH, "get");
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
				return r as StrictHttpResponse<PagedTagRead>;
			}),
		);
}

getAllTags.PATH = "/api/tag/";
