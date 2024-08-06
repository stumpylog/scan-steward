/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PagedPetReadSchema } from "../../models/paged-pet-read-schema";

export interface GetPets$Params {
	page?: number;
}

export function getPets(
	http: HttpClient,
	rootUrl: string,
	params?: GetPets$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<PagedPetReadSchema>> {
	const rb = new RequestBuilder(rootUrl, getPets.PATH, "get");
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
				return r as StrictHttpResponse<PagedPetReadSchema>;
			}),
		);
}

getPets.PATH = "/api/pet/";
