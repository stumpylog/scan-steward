/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { TagRead } from "../../models/tag-read";

export interface GetSingleTag$Params {
	tag_id: number;
}

export function getSingleTag(
	http: HttpClient,
	rootUrl: string,
	params: GetSingleTag$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<TagRead>> {
	const rb = new RequestBuilder(rootUrl, getSingleTag.PATH, "get");
	if (params) {
		rb.path("tag_id", params.tag_id, {});
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<TagRead>;
			}),
		);
}

getSingleTag.PATH = "/api/tag/{tag_id}/";
