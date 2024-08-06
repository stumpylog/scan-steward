/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { RoughDateReadSchema } from "../../models/rough-date-read-schema";
import { RoughDateUpdateSchema } from "../../models/rough-date-update-schema";

export interface UpdateRoughDate$Params {
	date_id: number;
	body: RoughDateUpdateSchema;
}

export function updateRoughDate(
	http: HttpClient,
	rootUrl: string,
	params: UpdateRoughDate$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<RoughDateReadSchema>> {
	const rb = new RequestBuilder(rootUrl, updateRoughDate.PATH, "patch");
	if (params) {
		rb.path("date_id", params.date_id, {});
		rb.body(params.body, "application/json");
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

updateRoughDate.PATH = "/api/date/{date_id}/";
