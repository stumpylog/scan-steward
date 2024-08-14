/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { TagCreate } from "../../models/tag-create";
import { TagRead } from "../../models/tag-read";

export interface CreateTag$Params {
	body: TagCreate;
}

export function createTag(
	http: HttpClient,
	rootUrl: string,
	params: CreateTag$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<TagRead>> {
	const rb = new RequestBuilder(rootUrl, createTag.PATH, "post");
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
				return r as StrictHttpResponse<TagRead>;
			}),
		);
}

createTag.PATH = "/api/tag/";
