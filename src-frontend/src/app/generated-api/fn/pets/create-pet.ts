/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PetCreateSchema } from "../../models/pet-create-schema";
import { PetReadSchema } from "../../models/pet-read-schema";

export interface CreatePet$Params {
	body: PetCreateSchema;
}

export function createPet(
	http: HttpClient,
	rootUrl: string,
	params: CreatePet$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<PetReadSchema>> {
	const rb = new RequestBuilder(rootUrl, createPet.PATH, "post");
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
				return r as StrictHttpResponse<PetReadSchema>;
			}),
		);
}

createPet.PATH = "/api/pet/";
