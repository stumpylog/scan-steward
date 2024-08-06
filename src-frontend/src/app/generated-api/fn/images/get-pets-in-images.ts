/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PetWithBoxSchema } from "../../models/pet-with-box-schema";

export interface GetPetsInImages$Params {
	image_id: number;
}

export function getPetsInImages(
	http: HttpClient,
	rootUrl: string,
	params: GetPetsInImages$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<Array<PetWithBoxSchema>>> {
	const rb = new RequestBuilder(rootUrl, getPetsInImages.PATH, "get");
	if (params) {
		rb.path("image_id", params.image_id, {});
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

getPetsInImages.PATH = "/api/image/{image_id}/pets/";
