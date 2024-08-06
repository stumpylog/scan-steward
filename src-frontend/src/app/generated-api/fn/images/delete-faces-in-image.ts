/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PersonFaceDeleteSchema } from "../../models/person-face-delete-schema";
import { PersonWithBoxSchema } from "../../models/person-with-box-schema";

export interface DeleteFacesInImage$Params {
	image_id: number;
	body: PersonFaceDeleteSchema;
}

export function deleteFacesInImage(
	http: HttpClient,
	rootUrl: string,
	params: DeleteFacesInImage$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<Array<PersonWithBoxSchema>>> {
	const rb = new RequestBuilder(rootUrl, deleteFacesInImage.PATH, "delete");
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
				return r as StrictHttpResponse<Array<PersonWithBoxSchema>>;
			}),
		);
}

deleteFacesInImage.PATH = "/api/image/{image_id}/faces/";
