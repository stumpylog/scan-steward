/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PersonReadSchema } from "../../models/person-read-schema";

export interface GetPerson$Params {
	person_id: number;
}

export function getPerson(
	http: HttpClient,
	rootUrl: string,
	params: GetPerson$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<PersonReadSchema>> {
	const rb = new RequestBuilder(rootUrl, getPerson.PATH, "get");
	if (params) {
		rb.path("person_id", params.person_id, {});
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<PersonReadSchema>;
			}),
		);
}

getPerson.PATH = "/api/person/{person_id}/";
