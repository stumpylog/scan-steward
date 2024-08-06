/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { TagRead } from "../../models/tag-read";
import { TagUpdate } from "../../models/tag-update";

export interface UpdateTag$Params {
	tag_id: number;
	body: TagUpdate;
}

export function updateTag(
	http: HttpClient,
	rootUrl: string,
	params: UpdateTag$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<TagRead>> {
	const rb = new RequestBuilder(rootUrl, updateTag.PATH, "patch");
	if (params) {
		rb.path("tag_id", params.tag_id, {});
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

updateTag.PATH = "/api/tag/{tag_id}/";
