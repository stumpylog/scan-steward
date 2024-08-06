/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { RoughDateCreateSchema } from "../../models/rough-date-create-schema";
import { RoughDateReadSchema } from "../../models/rough-date-read-schema";

export interface CreateRoughDate$Params {
	body: RoughDateCreateSchema;
}

export function createRoughDate(
	http: HttpClient,
	rootUrl: string,
	params: CreateRoughDate$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<RoughDateReadSchema>> {
	const rb = new RequestBuilder(rootUrl, createRoughDate.PATH, "post");
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
				return r as StrictHttpResponse<RoughDateReadSchema>;
			}),
		);
}

createRoughDate.PATH = "/api/date/";
