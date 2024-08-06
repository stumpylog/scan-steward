/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { ImageMetadataReadSchema } from "../../models/image-metadata-read-schema";

export interface GetImageMetadata$Params {
	image_id: number;
}

export function getImageMetadata(
	http: HttpClient,
	rootUrl: string,
	params: GetImageMetadata$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<ImageMetadataReadSchema>> {
	const rb = new RequestBuilder(rootUrl, getImageMetadata.PATH, "get");
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
				return r as StrictHttpResponse<ImageMetadataReadSchema>;
			}),
		);
}

getImageMetadata.PATH = "/api/image/{image_id}/metadata/";
