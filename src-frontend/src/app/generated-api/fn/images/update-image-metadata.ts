/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { ImageMetadataReadSchema } from "../../models/image-metadata-read-schema";
import { ImageMetadataUpdateSchema } from "../../models/image-metadata-update-schema";

export interface UpdateImageMetadata$Params {
	image_id: number;
	body: ImageMetadataUpdateSchema;
}

export function updateImageMetadata(
	http: HttpClient,
	rootUrl: string,
	params: UpdateImageMetadata$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<ImageMetadataReadSchema>> {
	const rb = new RequestBuilder(rootUrl, updateImageMetadata.PATH, "patch");
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
				return r as StrictHttpResponse<ImageMetadataReadSchema>;
			}),
		);
}

updateImageMetadata.PATH = "/api/image/{image_id}/metadata/";
