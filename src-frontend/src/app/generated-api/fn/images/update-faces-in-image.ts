/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PersonWithBoxSchema } from "../../models/person-with-box-schema";

export interface UpdateFacesInImage$Params {
	image_id: number;
	body: Array<PersonWithBoxSchema>;
}

export function updateFacesInImage(
	http: HttpClient,
	rootUrl: string,
	params: UpdateFacesInImage$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<Array<PersonWithBoxSchema>>> {
	const rb = new RequestBuilder(rootUrl, updateFacesInImage.PATH, "patch");
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

updateFacesInImage.PATH = "/api/image/{image_id}/faces/";
