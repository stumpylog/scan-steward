/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PetReadSchema } from "../../models/pet-read-schema";

export interface GetSinglePet$Params {
	pet_id: number;
}

export function getSinglePet(
	http: HttpClient,
	rootUrl: string,
	params: GetSinglePet$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<PetReadSchema>> {
	const rb = new RequestBuilder(rootUrl, getSinglePet.PATH, "get");
	if (params) {
		rb.path("pet_id", params.pet_id, {});
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<PetReadSchema>;
			}),
		);
}

getSinglePet.PATH = "/api/pet/{pet_id}/";
