/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { TagTree } from "../../models/tag-tree";

export interface GetTagTree$Params {
	name?: string | null;
}

export function getTagTree(
	http: HttpClient,
	rootUrl: string,
	params?: GetTagTree$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<Array<TagTree>>> {
	const rb = new RequestBuilder(rootUrl, getTagTree.PATH, "get");
	if (params) {
		rb.query("name", params.name, {});
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<Array<TagTree>>;
			}),
		);
}

getTagTree.PATH = "/api/tag/tree/";
