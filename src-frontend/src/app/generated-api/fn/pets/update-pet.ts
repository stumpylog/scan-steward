/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PetReadSchema } from "../../models/pet-read-schema";
import { PetUpdateSchema } from "../../models/pet-update-schema";

export interface UpdatePet$Params {
	pet_id: number;
	body: PetUpdateSchema;
}

export function updatePet(
	http: HttpClient,
	rootUrl: string,
	params: UpdatePet$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<PetReadSchema>> {
	const rb = new RequestBuilder(rootUrl, updatePet.PATH, "patch");
	if (params) {
		rb.path("pet_id", params.pet_id, {});
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

updatePet.PATH = "/api/pet/{pet_id}/";
