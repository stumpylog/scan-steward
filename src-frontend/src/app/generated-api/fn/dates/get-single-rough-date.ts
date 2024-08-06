/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { RoughDateReadSchema } from "../../models/rough-date-read-schema";

export interface GetSingleRoughDate$Params {
	date_id: number;
}

export function getSingleRoughDate(
	http: HttpClient,
	rootUrl: string,
	params: GetSingleRoughDate$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<RoughDateReadSchema>> {
	const rb = new RequestBuilder(rootUrl, getSingleRoughDate.PATH, "get");
	if (params) {
		rb.path("date_id", params.date_id, {});
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<RoughDateReadSchema>;
			}),
		);
}

getSingleRoughDate.PATH = "/api/date/{date_id}/";
