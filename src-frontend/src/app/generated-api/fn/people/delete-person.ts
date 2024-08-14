/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

export interface DeletePerson$Params {
	person_id: number;
}

export function deletePerson(
	http: HttpClient,
	rootUrl: string,
	params: DeletePerson$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<void>> {
	const rb = new RequestBuilder(rootUrl, deletePerson.PATH, "delete");
	if (params) {
		rb.path("person_id", params.person_id, {});
	}

	return http
		.request(rb.build({ responseType: "text", accept: "*/*", context }))
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return (r as HttpResponse<any>).clone({
					body: undefined,
				}) as StrictHttpResponse<void>;
			}),
		);
}

deletePerson.PATH = "/api/person/{person_id}/";
