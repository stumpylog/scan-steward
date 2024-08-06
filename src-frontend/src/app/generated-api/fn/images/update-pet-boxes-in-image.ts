/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PetWithBoxSchema } from "../../models/pet-with-box-schema";

export interface UpdatePetBoxesInImage$Params {
	image_id: number;
	body: Array<PetWithBoxSchema>;
}

export function updatePetBoxesInImage(
	http: HttpClient,
	rootUrl: string,
	params: UpdatePetBoxesInImage$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<Array<PetWithBoxSchema>>> {
	const rb = new RequestBuilder(rootUrl, updatePetBoxesInImage.PATH, "patch");
	if (params) {
		rb.path("image_id", params.image_id, {});
		rb.body(params.body, "application/json");
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<Array<PetWithBoxSchema>>;
			}),
		);
}

updatePetBoxesInImage.PATH = "/api/image/{image_id}/pets/";
